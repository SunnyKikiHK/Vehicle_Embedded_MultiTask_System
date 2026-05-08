"""
Vehicle Voice Assistant Server - Socket.IO + LangGraph Workflow.

This server maintains persistent TCP connections with vehicle clients via Socket.IO,
processing voice commands through the multi-task workflow.
"""

import os
import logging
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from socketio import AsyncServer, AsyncNamespace
from socketio.asgi import ASGIApp
from uvicorn import Config, Server

from src.db.redis_client import RedisClient
from src.agent.executor import get_executor, shutdown_executor
from workflow import workflow


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# Environment configuration
ARK_API_BASE = os.getenv("ARK_API_BASE")
ARK_API_KEY = os.getenv("ARK_API_KEY")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
SOCKETIO_CORS_ALLOWED_ORIGINS = os.getenv("SOCKETIO_CORS_ORIGINS", "*")

# Shared Redis client (initialized in lifespan)
_redis_client: RedisClient | None = None


def get_redis() -> RedisClient:
    """Get the shared Redis client instance."""
    if _redis_client is None:
        raise RuntimeError("Redis client not initialized. Call lifespan first.")
    return _redis_client


class VehicleNamespace(AsyncNamespace):
    """
    Socket.IO namespace for vehicle connections.

    Handles:
    - Persistent connection management per vehicle
    - Query processing with user isolation
    - Session state via Redis
    """

    async def on_connect(self, sid: str, environ: dict, auth: dict | None = None) -> bool:
        """
        Handle new vehicle connection.

        Args:
            sid: Socket session ID
            environ: Request environment
            auth: Optional authentication data

        Returns:
            True to accept connection, False to reject
        """
        vehicle_id = auth.get("vehicle_id") if auth else None
        user_id = auth.get("user_id", f"vehicle_{sid}") if auth else f"vehicle_{sid}"

        logger.info(f"[SocketIO] Vehicle connected: sid={sid}, vehicle_id={vehicle_id}, user_id={user_id}")

        # Store session data in Redis
        redis = get_redis()
        await redis.set(
            f"session:{sid}",
            {
                "vehicle_id": vehicle_id,
                "user_id": user_id,
                "sid": sid,
                "connected": True,
            },
            ex=3600,
        )

        # Initialize MCP connections for this user
        try:
            executor = get_executor()
            from src.constants import DEFAULT_SERVER_URLS
            for server_name, server_url in DEFAULT_SERVER_URLS.items():
                await executor._ensure_connection(user_id, server_name)
            logger.info(f"[SocketIO] MCP connections initialized for user={user_id}")
        except Exception as e:
            logger.warning(f"[SocketIO] Failed to pre-initialize MCP connections: {e}")

        await self.emit("connected", {
            "status": "connected",
            "session_id": sid,
            "user_id": user_id,
        }, room=sid)

        return True

    async def on_disconnect(self, sid: str) -> None:
        """Handle vehicle disconnection."""
        logger.info(f"[SocketIO] Vehicle disconnected: sid={sid}")

        # Clean up Redis session
        redis = get_redis()
        session_data = await redis.get(f"session:{sid}")

        if session_data:
            user_id = session_data.get("user_id")
            if user_id:
                # Disconnect user from all MCP servers
                try:
                    executor = get_executor()
                    await executor.disconnect_user(user_id)
                    logger.info(f"[SocketIO] MCP connections closed for user={user_id}")
                except Exception as e:
                    logger.warning(f"[SocketIO] Failed to close MCP connections: {e}")

        # Remove session from Redis
        await redis.set(f"session:{sid}", None)

    async def on_voice_query(self, sid: str, data: dict[str, Any]) -> dict[str, Any]:
        """
        Process voice query from vehicle.

        Expected data format:
        {
            "query": "帮我导航到最近的加油站",
            "language": "zh-CN",  # optional
            "metadata": {}  # optional
        }
        """
        logger.info(f"[SocketIO] Voice query received: sid={sid}, query={data.get('query', '')[:50]}...")

        # Get session data
        redis = get_redis()
        session_data = await redis.get(f"session:{sid}")

        if not session_data:
            return {
                "status": "error",
                "message": "Session not found. Please reconnect.",
            }

        query = data.get("query", "")
        user_id = session_data.get("user_id", f"vehicle_{sid}")
        metadata = data.get("metadata", {})

        if not query:
            return {
                "status": "error",
                "message": "Query is empty.",
            }

        try:
            # Emit processing status
            await self.emit("processing", {"status": "processing"}, room=sid)

            # Run the workflow
            result = await workflow.ainvoke({
                "query": query,
                "sender_id": user_id,
            })

            # Cache result in Redis
            redis = get_redis()
            await redis.set(
                f"query_history:{user_id}",
                {
                    "query": query,
                    "result": result,
                    "metadata": metadata,
                },
                ex=3600,
            )

            # Send result back
            await self.emit("response", {
                "status": "success",
                "query": query,
                "result": result,
            }, room=sid)

            logger.info(f"[SocketIO] Query processed successfully: sid={sid}")
            return {"status": "success", "result": result}

        except Exception as e:
            logger.error(f"[SocketIO] Error processing query: {e}", exc_info=True)
            await self.emit("error", {
                "status": "error",
                "message": f"Fail to process query: {str(e)}",
            }, room=sid)
            return {
                "status": "error",
                "message": str(e),
            }

    async def on_heartbeat(self, sid: str, data: dict | None = None) -> dict[str, Any]:
        """Handle heartbeat/keepalive from vehicle."""
        redis = get_redis()
        session_data = await redis.get(f"session:{sid}")

        if session_data:
            # Refresh TTL
            await redis.set(f"session:{sid}", session_data, ex=3600)

        return {
            "status": "ok",
            "sid": sid,
        }

    async def on_session_status(self, sid: str) -> dict[str, Any]:
        """Get current session status."""
        redis = get_redis()
        session_data = await redis.get(f"session:{sid}")

        if not session_data:
            return {"status": "disconnected"}

        return {
            "status": "connected",
            "session": session_data,
        }


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    global _redis_client

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

    # Initialize MCP executor
    try:
        await get_executor()
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
        allow_credentials=True,
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

    # Health check endpoint (health of the server)
    @app.get("/health")
    async def health():
        return {"status": "healthy"}

    # Configure Socket.IO
    sio = AsyncServer(
        async_mode="asgi",
        cors_allowed_origins=SOCKETIO_CORS_ALLOWED_ORIGINS.split(","), # for socket
        ping_timeout=60,
        ping_interval=25,
    )

    # Register namespace
    vehicle_namespace = VehicleNamespace("/vehicle") #name space path (the "suffix" or the "extension" after the mount path)
    sio.register_namespace(vehicle_namespace)

    # Mount Socket.IO ASGI app
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
    logger.info(f"[Server] Starting on {host}:{port}")
    server.run()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Vehicle Voice Assistant Server")
    parser.add_argument("--host", default="0.0.0.0", help="Server host")
    parser.add_argument("--port", type=int, default=8000, help="Server port")
    parser.add_argument("--log-level", default="info", choices=["debug", "info", "warning", "error"])

    args = parser.parse_args()

    run_server(host=args.host, port=args.port, log_level=args.log_level)
