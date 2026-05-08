"""MCP Executor - Wraps MCPClient for use in the workflow.

The executor provides a simple interface for agents to call MCP tools:
1. Each user gets isolated transport + session per server
2. Connections created on-demand per user-server pair
3. Provides unified call_tool interface
"""

import logging
import asyncio 
from typing import Any, Optional

from src.constants import DEFAULT_SERVER_URLS
from src.mcp.mcp_client import MCPClient
from src.mcp.mapping import get_server_for_tool

logger = logging.getLogger(__name__)


class MCPExecutor:
    """
    Executor that wraps MCPClient for use in the workflow.
    
    Each user gets isolated transport + session per server.
    Connections are created on-demand when a user first calls a tool.
    
    Usage:
        executor = MCPExecutor()
        
        # Call tool - connection created automatically if needed
        result = await executor.call_tool(
            tool_name="go_poi",
            slots={"destination": "加油站"},
            user_id="user_001"
        )
    """

    def __init__(self, server_urls: Optional[dict[str, str]] = None):
        """
        Initialize the executor.
        
        Args:
            server_urls: Optional dict mapping server names to URLs.
                        Defaults to DEFAULT_SERVER_URLS.
        """
        self._client = MCPClient()
        self._server_urls = server_urls or DEFAULT_SERVER_URLS.copy()

    async def call_tool(
        self,
        tool_name: str,
        slots: dict[str, Any],
        user_id: str,
        auth_token: Optional[str] = None,
    ) -> Any:
        """
        Call an MCP tool.
        
        Ensures connection exists for the user-server pair before calling.
        
        Args:
            tool_name: The name of the tool to call.
            slots: Dictionary of tool arguments.
            user_id: The user ID for session isolation.
            auth_token: Optional auth token for this connection.
            
        Returns:
            The tool result from the MCP server.
        """
        server_name = get_server_for_tool(tool_name)
        if not server_name:
            raise ValueError(f"Unknown tool: {tool_name}")

        await self._ensure_connection(user_id, server_name, auth_token)

        result = await self._client.call_tool( # result should be a dict with status, action, message, etc...
            tool_name=tool_name,
            user_id=user_id,
            server_name=server_name,
            arguments=slots,
        )
        return result

    async def list_tools(
        self,
        user_id: str,
        server_name: Optional[str] = None,
        auth_token: Optional[str] = None,
    ) -> list[Any]:
        """
        List available tools.
        
        Args:
            user_id: The user ID.
            server_name: Optional specific server. If None, uses first available.
            auth_token: Optional auth token.
        """
        if not server_name:
            server_name = next(iter(self._server_urls.keys()))

        await self._ensure_connection(user_id, server_name, auth_token)
        return await self._client.list_tools(user_id, server_name)

    async def _ensure_connection(
        self,
        user_id: str,
        server_name: str,
        auth_token: Optional[str] = None,
    ):
        """Ensure a connection exists for user-server pair."""
        if self._client.has_connection(user_id, server_name):
            return

        url = self._server_urls.get(server_name)
        if not url:
            raise ValueError(f"Unknown server: {server_name}")

        try:
            await self._client.connect(
                server_url=url,
                user_id=user_id,
                server_name=server_name,
                auth_token=auth_token,
            )
            logger.info(f"[Executor] Connected user '{user_id}' to '{server_name}'")
        except ValueError:
            pass  # Connection already exists (race condition handled)

    async def disconnect_user(self, user_id: str):
        """Disconnect all connections for a user."""
        await self._client.disconnect_user(user_id)
        logger.info(f"[Executor] Disconnected user '{user_id}' from all servers")

    async def cleanup(self):
        """Cleanup all resources."""
        await self._client.cleanup()
        logger.info("[Executor] Cleaned up all connections")


# Global executor instance
_executor: Optional[MCPExecutor] = None


def get_executor() -> MCPExecutor:
    """Get or create the global executor instance."""
    global _executor
    if _executor is None:
        _executor = MCPExecutor()
    return _executor


async def init_executor(server_urls: Optional[dict[str, str]] = None) -> MCPExecutor:
    """Initialize the global executor with optional custom server URLs."""
    global _executor
    _executor = MCPExecutor(server_urls)
    return _executor


async def shutdown_executor():
    """Shutdown the global executor."""
    global _executor
    if _executor is not None:
        await _executor.cleanup()
        _executor = None
