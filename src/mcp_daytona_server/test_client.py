# src/mcp_daytona_server/test_client.py
import asyncio
import httpx
from mcp_daytona_server.mcp_server import create_mcp_server, settings

async def test_server_connection():
    print("\nTesting Daytona server connection...")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{settings.mcp_daytona_server_url}/health",
                headers={
                    "Authorization": f"Bearer {settings.mcp_daytona_api_key}"
                }
            )
            print(f"Server response status: {response.status_code}")
            print(f"Server response: {response.text}")
        except Exception as e:
            print(f"Error connecting to server: {str(e)}")

async def test_server():
    # First test connection
    await test_server_connection()

    mcp = create_mcp_server()

    try:
        print("\nCreating Daytona environment...")
        # Try with a specific image
        result = await mcp.call_tool(
            "create_daytona_env",
            {
                "language": "python",
                #"image": "python:3.12",  # Specify an image
                #"os_user": "daytona",    # Specify user
                #"env_vars": {            # Add some env vars
                #    "PYTHONUNBUFFERED": "1"
                #}
            }
        )
        print(f"Result: {result}")

        if result:
            print("\nExecuting test code...")
            code_result = await mcp.call_tool(
                "execute_claude_code",
                {
                    "code": "print('Hello from Daytona!')",
                    "workspace_id": result
                }
            )
            print(f"Code execution result: {code_result}")

            print("\nCleaning up...")
            cleanup_result = await mcp.call_tool(
                "remove_daytona_env",
                {"workspace_id": result}
            )
            print(f"Cleanup result: {cleanup_result}")

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_server())