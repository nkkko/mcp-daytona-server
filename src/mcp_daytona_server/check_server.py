# /Users/nikola/dev/mcp-daytona-server/src/mcp_daytona_server/check_server.py
import asyncio
import httpx
from mcp_daytona_server.mcp_server import settings

async def check_server():
    print("\nChecking SDK configuration...")
    # print(f"Config: {daytona_client.config}")
    print("\nChecking Daytona server version...")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{settings.mcp_daytona_server_url}/version",
                headers={
                    "Authorization": f"Bearer {settings.mcp_daytona_api_key}",
                }
            )
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            print(f"Headers: {response.headers}")
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(check_server())