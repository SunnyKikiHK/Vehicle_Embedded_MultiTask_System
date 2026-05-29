"""MCP Executor - Wraps MCPClient for use in the workflow.

The executor provides a simple interface for agents to call MCP tools.
Uses connection-per-call pattern: each tool call creates a fresh HTTP connection
that is opened and closed within the same async task.
"""

import logging
from typing import Any, Optional

from src.constants import DEFAULT_SERVER_URLS, TOOL_METADATA_REQUIREMENTS
from src.mcp.mcp_client import MCPClient
from src.mcp.mapping import get_server_for_tool

logger = logging.getLogger(__name__)


class MCPExecutor:
    """
    Executor that wraps MCPClient for use in the workflow.
    
    Uses connection-per-call pattern: each tool call creates a fresh HTTP connection
    that is opened and closed within the same async task. This avoids anyio
    cancel-scope cross-task issues.
    
    Usage:
        executor = MCPExecutor()
        
        # Call tool - creates fresh connection per call
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
        
        # Configure server URLs in the client
        for name, url in self._server_urls.items():
            self._client.configure_server(name, url)

    async def call_tool(
        self,
        tool_name: str,
        slots: dict[str, Any],
        user_id: str,
        metadata: Optional[dict[str, Any]] = None,
        auth_token: Optional[str] = None,
    ) -> Any:
        """
        Call an MCP tool.
        
        Creates a fresh connection for this call to avoid cross-task issues.
        
        Args:
            tool_name: The name of the tool to call.
            slots: Dictionary of tool arguments.
            user_id: The user ID for logging purposes.
            metadata: Optional metadata dict containing vehicle_id, etc.
            auth_token: Optional auth token (passed to MCP server).
            
        Returns:
            The tool result from the MCP server.
        """
        logger.info(f"[Executor] call_tool: tool={tool_name}, user_id={user_id}")
        server_name = get_server_for_tool(tool_name)
        if not server_name:
            raise ValueError(f"Unknown tool: {tool_name}")
        
        server_url = self._server_urls.get(server_name)
        if not server_url:
            raise ValueError(f"No URL configured for server: {server_name}")
        
        # Check if this tool requires metadata
        requires_metadata = TOOL_METADATA_REQUIREMENTS.get(server_name, {}).get(tool_name, False)
        
        # Prepare tool metadata if required
        tool_metadata = None
        if requires_metadata:
            tool_metadata = metadata or {}
            # Always include vehicle_id if not present
            if "vehicle_id" not in tool_metadata and user_id:
                tool_metadata["vehicle_id"] = user_id
            logger.info(f"[Executor] Tool {tool_name} requires metadata: {tool_metadata}")
        
        # Call tool - connection is created and closed within this method
        result = await self._client.call_tool(
            tool_name=tool_name,
            user_id=user_id,
            server_name=server_name,
            server_url=server_url,
            arguments=slots,
            metadata=tool_metadata,
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

        server_url = self._server_urls.get(server_name)
        if not server_url:
            raise ValueError(f"No URL configured for server: {server_name}")
        
        return await self._client.list_tools(
            user_id=user_id,
            server_name=server_name,
            server_url=server_url,
        )

    async def disconnect_user(self, user_id: str):
        """No-op for compatibility. Connections are closed per-call."""
        logger.debug(f"[Executor] disconnect_user called (no-op in per-call mode): user={user_id}")

    async def cleanup(self):
        """No-op for compatibility. Connections are closed per-call."""
        logger.debug("[Executor] cleanup called (no-op in per-call mode)")


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
