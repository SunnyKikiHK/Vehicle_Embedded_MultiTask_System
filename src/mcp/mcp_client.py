import asyncio
from typing import Dict, List, Any
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPClient:
    def __init__(self):
        self.exit_stack = AsyncExitStack()
        self.sessions: Dict[str, ClientSession] = {}
        self.server_scripts: Dict[str, str] = {}

    async def connect_to_server(self, server_name: str, server_script: str):
        is_python = server_script.endswith('.py')
        is_js = server_script.endswith('.js')

        if not is_python and not is_js:
            raise ValueError("Invalid MCP Server Script, must end with .py or .js")

        if server_name in self.sessions:
            raise ValueError(f"Server '{server_name}' already connected")

        command = "python" if is_python else "node"
        server_params = StdioServerParameters(
            command=command,
            args=[server_script],
            env=None
        )

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        read_stream, write_stream = stdio_transport
        session = await self.exit_stack.enter_async_context(
            ClientSession(read_stream, write_stream)
        )

        await session.initialize()
        self.sessions[server_name] = session
        self.server_scripts[server_name] = server_script

    async def connect_all_servers(self, server_configs: Dict[str, str]):
        for server_name, server_script in server_configs.items():
            await self.connect_to_server(server_name, server_script)

    async def disconnect_from_server(self, server_name: str):
        if server_name in self.sessions:
            await self.sessions[server_name].close()
            del self.sessions[server_name]
            if server_name in self.server_scripts:
                del self.server_scripts[server_name]

    async def process_query(self, server_name: str, query: str) -> Any:
        if server_name not in self.sessions:
            raise ValueError(f"Server '{server_name}' not connected")
        session = self.sessions[server_name]
        return await session.call_tool(query)

    async def get_available_servers(self) -> List[str]:
        return list(self.sessions.keys())

    async def cleanup(self):
        await self.exit_stack.aclose()
        self.sessions.clear()
        self.server_scripts.clear()


async def main():
    pass


if __name__ == "__main__":
    asyncio.run(main())