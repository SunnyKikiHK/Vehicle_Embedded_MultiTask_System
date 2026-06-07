"""
Vehicle Voice Assistant Server - Socket.IO + LangGraph Workflow.

This server maintains persistent TCP connections with vehicle clients via Socket.IO,
processing voice commands through the multi-task workflow.
"""

import os
import logging
from contextlib import asynccontextmanager
from typing import Any
from workflow import workflow
from src.db.redis_client import RedisClient
from src.agent.executor import get_executor, shutdown_executor
from src.context.location_provider import init_location_provider, get_location_provider
from src.context.location_store import LOCATION_TTL_SECONDS
from src.constants import SERVER_LOG_PATH

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from socketio import AsyncServer
from socketio.asgi import ASGIApp
from uvicorn import Config, Server

# In-memory store for socket auth data (sid -> auth dict) on the default namespace.
# This bridges the gap between on_connect (which receives auth) and other handlers.
_sio_auth_store: dict[str, dict] = {}

# Module-level AsyncServer instance; set inside create_app() so handler functions
# can reference it directly via `sio.emit(..., to=sid)`.
sio: AsyncServer | None = None


def setup_file_logging():
    """Configure file logging for the application."""
    # Check if we already have this file handler to avoid duplicates
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        if isinstance(handler, logging.FileHandler) and handler.baseFilename.endswith('server.log'):
            return handler  # Already configured
    
    # Ensure log directory exists
    log_dir = os.path.dirname(SERVER_LOG_PATH)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    
    # Create file handler
    file_handler = logging.FileHandler(SERVER_LOG_PATH, mode='a')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    ))
    
    # Add handler to root logger (not basicConfig, to ensure it works with uvicorn)
    root_logger.addHandler(file_handler)
    root_logger.setLevel(logging.INFO)
    
    return file_handler

logger = logging.getLogger(__name__)


# Environment configuration
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
SOCKETIO_CORS_ALLOWED_ORIGINS = "*"

# Shared Redis client (initialized in lifespan)
_redis_client: RedisClient | None = None

_LAST_N_HISTORY_TURNS = int(os.getenv("LAST_N_HISTORY_TURNS", "5"))
_SESSION_EXP_TIMEOUT = 3600 # Use heartbeat to update expire time
_HISTORY_EXP_TIMEOUT = 3600

SAMPLE_KEY_FORMAT = "voice:last_service:{user_id}:history"  # Matches ReconstructionRouter's key pattern
SESSION_KEY_FORMAT = "session:{sid}"


def get_redis() -> RedisClient:
    """Get the shared Redis client instance."""
    if _redis_client is None:
        raise RuntimeError("Redis client not initialized. Call lifespan first.")
    return _redis_client


# Socket.IO event handlers (registered on the default namespace "/")

async def _on_connect(sid: str, environ: dict, auth: dict | None = None) -> bool:
    """
    Handle new vehicle connection.

    Args:
        sid: Socket session ID
        environ: Request environment
        auth: Optional authentication data passed from client

    Returns:
        True to accept connection, False to reject
    """
    try:
        print(f"!!! DEBUG on_connect called: sid={sid}, auth={auth}")
        print(f"!!! DEBUG Request path: {environ.get('PATH_INFO', 'N/A')}")
        logger.info(f"[SocketIO] on_connect called: sid={sid}, auth={auth}")
        logger.info(f"[SocketIO] Request headers: {dict(environ.get('headers', []))}")

        vehicle_id = auth.get("vehicle_id") if auth else None
        user_id = auth.get("user_id", f"vehicle_{sid}") if auth else f"vehicle_{sid}"
        logger.info(f"[SocketIO] vehicle_id={vehicle_id}, user_id={user_id}")

        if not vehicle_id or not user_id:
            logger.error(f"[SocketIO] Connection REJECTED: Invalid vehicle or user ID: vehicle_id={vehicle_id}, user_id={user_id}")
            await sio.emit("error", {
                "status": "error",
                "message": "Invalid vehicle or user ID.",
            }, to=sid)
            return False

        # Store auth data so other handlers can retrieve it via sid
        _sio_auth_store[sid] = {"vehicle_id": vehicle_id, "user_id": user_id}

        # Store session data in Redis
        redis = get_redis()
        await redis.set(
            SESSION_KEY_FORMAT.format(sid=sid),
            {
                "vehicle_id": vehicle_id,
                "user_id": user_id,
                "sid": sid,
                "connected": True,
            },
            ex=_SESSION_EXP_TIMEOUT,
        )

        # MCP connections are established lazily when tools are called
        # See executor._ensure_connection() which is called during tool execution
        # This avoids anyio cancel scope issues with MCP client

        await sio.emit("connected", {
            "status": "connected",
            "session_id": sid,
            "user_id": user_id,
            "gps_ttl_seconds": LOCATION_TTL_SECONDS,
        }, to=sid)

        logger.info(f"[SocketIO] Emitted 'connected' event to sid={sid}")

        logger.info(f"[SocketIO] Vehicle connected successfully: sid={sid}, vehicle_id={vehicle_id}, user_id={user_id}")
        return True

    except Exception as e:
        logger.error(f"[SocketIO] Exception in on_connect: sid={sid}, error={e}", exc_info=True)
        return False


async def _on_disconnect(sid: str) -> None:
    """Handle vehicle disconnection."""
    logger.info(f"[SocketIO] Vehicle disconnected: sid={sid}")
    try:
        # Clean up Redis session
        redis = get_redis()
        session_data = await redis.get(SESSION_KEY_FORMAT.format(sid=sid))

        if session_data:
            user_id = session_data.get("user_id")
            if user_id:
                # Note: MCP connections are now per-call, so no cleanup needed here
                logger.debug(f"[SocketIO] User disconnected: user_id={user_id}")

        # Remove session from Redis
        await redis.unlink(SESSION_KEY_FORMAT.format(sid=sid))

        # Clean up auth store
        _sio_auth_store.pop(sid, None)
    except Exception as e:
        logger.warning(f"[SocketIO] Exception in on_disconnect: sid={sid}, error={e}")


async def _on_voice_query(sid: str, data: dict[str, Any]) -> dict[str, Any]:
    """
    Process voice query from vehicle.

    Expected data format:
    {
        "query": "帮我导航到最近的加油站",
        "metadata": {},       // optional
        "stream": false,      // optional, whether to stream the response
        "react_mode": false    // optional, enable retry-on-failure ReAct loop
    }
    """
    logger.info(f"[SocketIO] Voice query received: sid={sid}, query={data.get('query', '')[:50]}...")

    # Get session data
    redis = get_redis()
    session_data = await redis.get(SESSION_KEY_FORMAT.format(sid=sid))

    if not session_data:
        return {
            "status": "error",
            "message": "Session not found. Please reconnect.",
        }
    logger.info(f"[SocketIO] Voice query session_data: {session_data}")
    query = data.get("query", "")
    user_id = session_data.get("user_id", f"vehicle_{sid}")
    vehicle_id = session_data.get("vehicle_id", user_id)  # Use vehicle_id for location lookup
    metadata = data.get("metadata", {})
    stream_mode = data.get("stream", False)
    react_mode = data.get("react_mode", False)

    if not query:
        return {
            "status": "error",
            "message": "Query is empty.",
        }

    try:
        # Emit processing status
        await sio.emit("processing", {"status": "processing"}, to=sid)

        # Load history from Redis (returns list of query/result dicts)
        history = await redis.range_list(SAMPLE_KEY_FORMAT.format(user_id=user_id), 0, _LAST_N_HISTORY_TURNS)
        logger.info(f"[SocketIO] Voice query history: {history}")

        ### WE CAN EITHER GET GPS LOCATION IN HERE OR LET MCP SERVER TO GET THE LOCATION BY ITSELF IN ITS SERVER
        ### NOW WE LET MCP SERVER TO GET IT.
        # Get GPS location from LocationProvider (using vehicle_id to match _on_gps_update)
        # try:
        #     location_provider = get_location_provider()
        #     location_ctx = await location_provider.get_current_location(vehicle_id)
        #     if location_ctx:
        #         gps_data = {"latitude": location_ctx.latitude, "longitude": location_ctx.longitude}
        #         metadata = {**metadata, "gps_location": gps_data}
        #         logger.info(f"[SocketIO] GPS location for vehicle_id={vehicle_id}: {gps_data}")
        # except Exception as e:
        #     logger.warning(f"[SocketIO] Failed to get GPS location: {e}")
        
        metadata = {**metadata, "vehicle_id": vehicle_id}
        # Prepare workflow input
        workflow_input = {
            "query": query,
            "user_id": user_id,
            "last_n_history": history,
            "history_turns": _LAST_N_HISTORY_TURNS,
            "stream_mode": stream_mode,
            "sid": sid,
            "metadata": metadata,
            "react_mode": react_mode,
        }

        # Run the workflow
        result = None  # Initialize for streaming mode where "value" may not be emitted
        if stream_mode:
            # Streaming mode: use custom stream mode with get_stream_writer
            async for mode, event in workflow.astream(
                workflow_input,
                stream_mode=["custom", "values"]
                ):
                if mode == "custom":
                    await sio.emit("stream_response", {
                        "status": "streaming",
                        "chunk": event,
                        "query": query,
                    }, to=sid)
                elif mode == "values":
                    logger.info(f"[SocketIO] Voice query result 1: {event}")
                    result = event
        else:
            # Non-streaming mode
            result = await workflow.ainvoke(workflow_input)
        logger.info(f"[SocketIO] Voice query result 2: {result}")
        # Send result back (always sent at the end)
        await sio.emit("response", {
            "status": "success",
            "query": query,
            "result": result,
        }, to=sid)

        # Store query result in Redis (JSON format, bounded by trim_list)
        await redis.lpush(
            SAMPLE_KEY_FORMAT.format(user_id=user_id),
            {
                "query": result.get("reconstruction", {}).get("reconstructed_query", query),
                "intent": result.get("agent", {}).get("tool_name", ""),
                "slots": result.get("agent", {}).get("tool_args", {}),
                "response": result.get("response", ""),
                "metadata": metadata,
            },
            ex=_HISTORY_EXP_TIMEOUT,
        )

        # Trim to keep only last N entries (bounded history)
        await redis.trim_list(
            SAMPLE_KEY_FORMAT.format(user_id=user_id),
            0,
            _LAST_N_HISTORY_TURNS,
        )

        logger.info(f"[SocketIO] Query processed successfully: sid={sid}")
        return {"status": "success", "result": result}

    except Exception as e:
        logger.error(f"[SocketIO] Error processing query: {e}", exc_info=True)
        await sio.emit("error", {
            "status": "error",
            "message": f"Fail to process query: {str(e)}",
        }, to=sid)
        return {
            "status": "error",
            "message": str(e),
        }


async def _on_heartbeat(sid: str, data: dict | None = None) -> dict[str, Any]:
    """Handle heartbeat/keepalive from vehicle."""
    redis = get_redis()
    session_data = await redis.get(SESSION_KEY_FORMAT.format(sid=sid))

    if session_data:
        # Refresh TTL
        await redis.set(SESSION_KEY_FORMAT.format(sid=sid), session_data, ex=_SESSION_EXP_TIMEOUT)

    return {
        "status": "ok",
        "sid": sid,
    }


async def _on_session_status(sid: str) -> dict[str, Any]:
    """Get current session status."""
    redis = get_redis()
    session_data = await redis.get(SESSION_KEY_FORMAT.format(sid=sid))

    if not session_data:
        return {"status": "disconnected"}

    return {
        "status": "connected",
        "session": session_data,
    }


async def _on_gps_update(sid: str, data: dict[str, Any]) -> dict[str, Any]:
    """
    Handle GPS update from vehicle/client.
    
    Expected data format:
    {
        "latitude": 39.9042,
        "longitude": 116.4074,
        "active": true
    }
    or
    {
        "active": false
    }
    """
    # Get session data to get vehicle_id
    redis = get_redis()
    session_data = await redis.get(SESSION_KEY_FORMAT.format(sid=sid))
    
    if not session_data:
        return {"status": "error", "message": "Session not found. Please reconnect."}
    
    vehicle_id = session_data.get("vehicle_id")
    if not vehicle_id:
        return {"status": "error", "message": "Vehicle ID not found in session"}
    
    location_provider = get_location_provider()
    active = data.get("active", False)
    
    if not active:
        # Deactivate GPS - clear location from LocationProvider
        await location_provider.deactivate_gps(vehicle_id)
        logger.info(f"[SocketIO] GPS deactivated for sid={sid}, vehicle_id={vehicle_id}")
        return {"status": "success", "message": "GPS deactivated"}
    
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    
    if latitude is None or longitude is None:
        return {"status": "error", "message": "Missing latitude or longitude"}
    
    # Store GPS location using LocationProvider
    await location_provider.update_location(
        vehicle_id=vehicle_id,
        latitude=float(latitude),
        longitude=float(longitude)
    )
    
    logger.info(f"[SocketIO] GPS updated for sid={sid}, vehicle_id={vehicle_id}: ({latitude}, {longitude})")
    
    return {
        "status": "success",
        "message": "GPS location updated",
        "data": {"latitude": float(latitude), "longitude": float(longitude)},
        "ttl_seconds": LOCATION_TTL_SECONDS,
    }


# Application lifespan

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    global _redis_client

    # Ensure file logging is set up
    setup_file_logging()
    
    logger.info("[App] Starting Vehicle Voice Assistant Server...")

    # Initialize Redis pool and client
    try:
        await RedisClient.create_pool(
            host=REDIS_HOST,
            port=REDIS_PORT,
        )
        _redis_client = RedisClient(host=REDIS_HOST, port=REDIS_PORT)
        logger.info(f"[App] Redis pool and client created: {REDIS_HOST}:{REDIS_PORT}")
    except Exception as e:
        logger.warning(f"[App] Redis connection failed: {e}. Running without Redis caching.")

    # Initialize LocationProvider
    try:
        init_location_provider(_redis_client)
        logger.info("[App] LocationProvider initialized")
    except Exception as e:
        logger.error(f"[App] LocationProvider initialization failed: {e}")

    # Initialize MCP executor
    try:
        get_executor()
        logger.info("[App] MCP Executor initialized")
    except Exception as e:
        logger.error(f"[App] MCP Executor initialization failed: {e}")

    logger.info("[App] Server ready")

    yield

    # Cleanup
    logger.info("[App] Shutting down...")
    await RedisClient.close_pool()
    logger.info("[App] Redis pool closed")
    await shutdown_executor()
    logger.info("[App] MCP Executor closed")
    logger.info("[App] Shutdown complete")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Vehicle Voice Assistant API",
        description="Multi-task voice assistant for vehicle embedded systems",
        version="1.0.0",
        lifespan=lifespan,
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=SOCKETIO_CORS_ALLOWED_ORIGINS.split(","), # for http
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Root endpoint
    @app.get("/")
    async def root():
        return {
            "service": "Vehicle Voice Assistant",
            "status": "running",
            "version": "1.0.0",
        }
    # Configure Socket.IO
    global sio
    sio = AsyncServer(
        async_mode="asgi",
        cors_allowed_origins="*",
        ping_timeout=60,
        ping_interval=25,
        logger=True,
        engineio_logger=True,
    )

    # Register event handlers on the default namespace "/" directly.
    # auth data received in on_connect is stored in _sio_auth_store for lookup
    # by downstream handlers.
    sio.on("connect", _on_connect)
    sio.on("disconnect", _on_disconnect)
    sio.on("voice_query", _on_voice_query)
    sio.on("heartbeat", _on_heartbeat)
    sio.on("session_status", _on_session_status)
    sio.on("gps_update", _on_gps_update)

    # Mount Socket.IO ASGI app at /socket.io
    print("!!! DEBUG: Mounting Socket.IO at / (default namespace)")
    app.mount("/", ASGIApp(sio))

    return app


def run_server(host: str = "0.0.0.0", port: int = 8000, log_level: str = "info"):
    """Run the server using Uvicorn."""
    config = Config(
        app=create_app(),
        host=host,
        port=port,
        log_level=log_level,
    )
    server = Server(config)
    server.run()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Vehicle Voice Assistant Server")
    parser.add_argument("--host", default="0.0.0.0", help="Server host")
    parser.add_argument("--port", type=int, default=8000, help="Server port")
    parser.add_argument("--log-level", default="info", choices=["debug", "info", "warning", "error"])

    args = parser.parse_args()

    run_server(host=args.host, port=args.port, log_level=args.log_level)
