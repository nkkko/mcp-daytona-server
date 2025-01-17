# src/main.py
import asyncio

from .mcp_server import create_mcp_server

async def main():
  mcp = create_mcp_server()
  await mcp.run()

if __name__ == "__main__":
  anyio.run(main, backend="trio")