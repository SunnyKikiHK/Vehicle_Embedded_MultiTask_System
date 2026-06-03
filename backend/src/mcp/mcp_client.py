import json
import logging
from typing import Any, Optional

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

logger = logging.getLogger(__name__)


class MCPClient:
    """
    MCP Client with connection-per-call pattern.
    
    Each tool call creates a fresh HTTP connection that is opened and closed
    within the same async task. This avoids anyio cancel-scope cross-task
    RuntimeError issues that occur with persistent sessions.
    
    Note: HTTP/1.1 keep-alive is used automatically by the underlying HTTP client,
    so there's no overhead of establishing a new TCP connection for each call.
    """

    def __init__(self):
        self._server_urls: dict[str, str] = {}

    def configure_server(self, server_name: str, server_url: str) -> None:
        """Configure the URL for a named server."""
        self._server_urls[server_name] = server_url

    async def call_tool(
        self,
        tool_name: str,
        user_id: str,
        server_name: str,
        server_url: Optional[str] = None,
        arguments: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Any:
        """
        Call a tool on the MCP server with a fresh connection.
        
        Creates a new HTTP connection for each call to avoid cross-task cancel scope issues.
        
        Args:
            tool_name: The name of the tool to call
            user_id: User identifier (for logging purposes)
            server_name: Server name to look up URL if not provided
            server_url: Optional explicit server URL
            arguments: Tool arguments
            metadata: Optional metadata dict (vehicle_id, etc.)
            
        Returns:
            Parsed JSON object from the first text content block, or None.
        """
        url = server_url or self._server_urls.get(server_name)
        if not url:
            raise ValueError(f"No URL configured for server '{server_name}'")
        
        logger.info(f"call_tool: user={user_id}, tool={tool_name}, server={server_name}, metadata={metadata}")
        
        # Merge metadata into arguments if provided
        tool_args = arguments or {}
        if metadata:
            # Add metadata to arguments (MCP tool will receive it as metadata parameter)
            tool_args["metadata"] = metadata
        
        async with streamable_http_client(url=url) as (read_stream, write_stream, _get_session_id):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                result = await session.call_tool(tool_name, tool_args)
                logger.info(f"[MCPClient]call_tool result: {result}")
                if not result.isError and result.content:
                    text_block = result.content[0]
                    if getattr(text_block, "type", None) == "text":
                        return json.loads(text_block.text)
                else:
                    logger.error(f"[MCPClient]call_tool has error: {result}")
                    return None
        
        return {
            "message": "Server error",
        }

    async def list_tools(
        self,
        user_id: str,
        server_name: str,
        server_url: Optional[str] = None,
    ) -> list[Any]:
        """
        List available tools with a fresh connection.
        
        Args:
            user_id: User identifier (for logging purposes)
            server_name: Server name to look up URL
            server_url: Optional explicit server URL
            
        Returns:
            List of available tools.
        """
        url = server_url or self._server_urls.get(server_name)
        if not url:
            raise ValueError(f"No URL configured for server '{server_name}'")
        
        logger.info(f"list_tools: user={user_id}, server={server_name}")
        
        async with streamable_http_client(url=url) as (read_stream, write_stream, _get_session_id):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                result = await session.list_tools()
                return result.tools if hasattr(result, "tools") else result

    async def cleanup(self) -> None:
        """No-op for compatibility. Connections are closed per-call."""
        pass


async def main():
    pass


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
