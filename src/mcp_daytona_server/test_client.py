# /Users/nikola/dev/mcp-daytona-server/src/mcp_daytona_server/test_client.py
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
    workspace_id = None

    try:
        print("\nCreating Daytona environment...")
        workspace_id = await mcp.call_tool(
            "create_daytona_env",
            {
                "language": "python",
                "env_vars": {
                    "PYTHONUNBUFFERED": "1"
                }
            }
        )
        print(f"Created workspace: {workspace_id}")

        print("\nWaiting for workspace to be ready...")
        await asyncio.sleep(5)

        print("\nExecuting test code...")
        code_result = await mcp.call_tool(
            "execute_claude_code",
            {
                "code": 'print("Hello from Daytona!")',
                "workspace_id": workspace_id
            }
        )

        # Extract the actual output from the result
        output = code_result[0].text if isinstance(code_result, list) else code_result
        print(f"Code output: {output}")

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

    finally:
        if workspace_id:
            print("\nCleaning up...")
            try:
                cleanup_result = await mcp.call_tool(
                    "remove_daytona_env",
                    {"workspace_id": workspace_id}
                )
                # Extract cleanup message
                cleanup_msg = cleanup_result[0].text if isinstance(cleanup_result, list) else cleanup_result
                print(f"Cleanup: {cleanup_msg}")
            except Exception as e:
                print(f"Error during cleanup: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_server())