import asyncio
from typing import Any, Optional
from contextlib import AsyncExitStack
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


class MCPClient:
    """
    MCP Client with per-user-per-server transport isolation.
    
    Each user gets their own transport (HTTP connection) to each server,
    ensuring no message interleaving when multiple users call tools simultaneously.
    
    Structure: {(user_id, server_name): (transport_streams, session)}
    """

    def __init__(self):
        self.exit_stack = AsyncExitStack()
        # Each (user_id, server_name) maps to its own transport + session
        # {(user_id, server_name): {"streams": (read, write), "session": ClientSession}}
        self._connections: dict[tuple[str, str], dict[str, Any]] = {}

    def _make_key(self, user_id: str, server_name: str) -> tuple[str, str]:
        """Create a unique key for a user-server pair."""
        return (user_id, server_name)

    async def connect(
        self,
        server_url: str,
        user_id: str,
        server_name: str,
        auth_token: Optional[str] = None,
    ):
        """
        Connect to an MCP server for a specific user.
        Creates a dedicated transport and session for this user-server pair.

        Args:
            server_url: The URL of the MCP server (e.g., "http://localhost:8000/mcp")
            user_id: Unique identifier for the user
            server_name: Logical server name (e.g., "nav_server")
            auth_token: Optional authentication token
        """
        key = self._make_key(user_id, server_name)
        
        if key in self._connections:
            raise ValueError(f"Connection for user '{user_id}' to server '{server_name}' already exists")

        headers = {}
        if auth_token:
            headers["Authorization"] = f"Bearer {auth_token}"

        streams = await self.exit_stack.enter_async_context(
            streamable_http_client(server_url, headers=headers)
        )
        read_stream, write_stream = streams

        session = await self.exit_stack.enter_async_context(
            ClientSession(read_stream, write_stream)
        )
        await session.initialize()

        self._connections[key] = {
            "streams": streams,
            "session": session,
            "server_url": server_url,
        }

    async def disconnect(self, user_id: str, server_name: str):
        """
        Disconnect a user's connection to a specific server.
        
        Args:
            user_id: The user ID
            server_name: The server name
        """
        key = self._make_key(user_id, server_name)
        
        if key not in self._connections:
            raise ValueError(f"No connection found for user '{user_id}' to server '{server_name}'")

        session = self._connections[key]["session"]
        await session.close()
        del self._connections[key]

    async def disconnect_user(self, user_id: str):
        """
        Disconnect all connections for a user.
        
        Args:
            user_id: The user ID
        """
        keys_to_remove = [
            key for key in self._connections.keys() if key[0] == user_id
        ]
        for key in keys_to_remove:
            await self.disconnect(key[0], key[1])

    async def call_tool(
        self,
        tool_name: str,
        user_id: str,
        server_name: str,
        arguments: dict[str, Any] | None = None,
    ) -> Any:
        """
        Call a tool on the MCP server.

        Args:
            tool_name: The name of the tool to call.
            user_id: The user ID.
            server_name: The server name.
            arguments: Optional dictionary of tool arguments.

        Returns:
            The tool result from the MCP server.
        """
        key = self._make_key(user_id, server_name)
        
        if key not in self._connections:
            raise ValueError(
                f"No connection for user '{user_id}' to server '{server_name}'. "
                "Call connect() first."
            )

        session = self._connections[key]["session"]
        return await session.call_tool(tool_name, arguments or {})

    async def list_tools(self, user_id: str, server_name: str) -> list[Any]:
        """
        List available tools for a user-server connection.

        Args:
            user_id: The user ID.
            server_name: The server name.
        """
        key = self._make_key(user_id, server_name)
        
        if key not in self._connections:
            raise ValueError(
                f"No connection for user '{user_id}' to server '{server_name}'. "
                "Call connect() first."
            )

        session = self._connections[key]["session"]
        result = await session.list_tools()
        return result.tools if hasattr(result, 'tools') else result

    def has_connection(self, user_id: str, server_name: str) -> bool:
        """Check if a connection exists for user-server pair."""
        key = self._make_key(user_id, server_name)
        return key in self._connections

    def get_active_users(self) -> list[str]:
        """Get list of active user IDs."""
        return list(set(key[0] for key in self._connections.keys()))

    def get_active_servers(self) -> list[str]:
        """Get list of active server names for current connections."""
        return list(set(key[1] for key in self._connections.keys()))

    async def cleanup(self):
        """Close all connections and cleanup resources."""
        for key in list(self._connections.keys()):
            try:
                session = self._connections[key]["session"]
                await session.close()
            except Exception:
                pass
        self._connections.clear()
        await self.exit_stack.aclose()


async def main():
    pass


if __name__ == "__main__":
    asyncio.run(main())
