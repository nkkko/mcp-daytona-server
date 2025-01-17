# src/mcp_daytona_server/list_configs.py
import asyncio
import httpx
from mcp_daytona_server.mcp_server import settings

async def list_configurations():
    print("\nListing workspaces...")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{settings.mcp_daytona_server_url}/workspaces",
                headers={
                    "Authorization": f"Bearer {settings.mcp_daytona_api_key}",
                    "Accept": "application/json"
                }
            )
            print(f"Server response status: {response.status_code}")
            print(f"Server response: {response.text}")
        except Exception as e:
            print(f"Error getting workspaces: {str(e)}")

    print("\nGetting providers...")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{settings.mcp_daytona_server_url}/providers",
                headers={
                    "Authorization": f"Bearer {settings.mcp_daytona_api_key}",
                    "Accept": "application/json"
                }
            )
            print(f"Server response status: {response.status_code}")
            print(f"Server response: {response.text}")
        except Exception as e:
            print(f"Error getting providers: {str(e)}")

    # Try creating a workspace directly via API to see the full request/response
    print("\nTrying to create workspace directly...")
    async with httpx.AsyncClient() as client:
        try:
            workspace_data = {
                "language": "python",
                "provider": "local",
                "config": {
                    "image": "python:3.12-slim",
                    "run_as_user": "root"
                }
            }
            response = await client.post(
                f"{settings.mcp_daytona_server_url}/workspaces",
                headers={
                    "Authorization": f"Bearer {settings.mcp_daytona_api_key}",
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                json=workspace_data
            )
            print(f"Server response status: {response.status_code}")
            print(f"Server response: {response.text}")
            print(f"Response headers: {response.headers}")
        except Exception as e:
            print(f"Error creating workspace: {str(e)}")

if __name__ == "__main__":
    asyncio.run(list_configurations())