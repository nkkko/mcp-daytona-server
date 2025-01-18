# src/mcp_daytona_server/mcp_server.py
import os
import json  # Add this import
import httpx
import asyncio
from typing import Dict, Optional
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from mcp.server.fastmcp import FastMCP, Context

class Settings(BaseSettings):
    """Settings for the FastAPI server."""
    model_config = SettingsConfigDict(
        env_file=".env.local",
        extra="allow"
    )

    mcp_daytona_api_key: str
    mcp_daytona_server_url: str
    mcp_daytona_target: str = "local"

    def __str__(self):
        return f"""
        Daytona Settings:
        API Key: {self.mcp_daytona_api_key[:8]}...
        Server URL: {self.mcp_daytona_server_url}
        Target: {self.mcp_daytona_target}
        """

load_dotenv()
settings = Settings()
print(settings)

def create_mcp_server() -> FastMCP:
    mcp = FastMCP(name="Daytona MCP", description="MCP Server with Daytona integration.")


    @mcp.tool()
    async def create_daytona_env(
        language: str = "python",
        image: Optional[str] = None,
        os_user: Optional[str] = None,
        env_vars: Optional[Dict[str, str]] = None
    ) -> str:
        """Creates a new Daytona development environment."""
        try:
            # Generate a unique workspace ID
            workspace_id = f"mcp-workspace-{os.urandom(4).hex()}"

            # Create a unique repository ID
            repo_id = f"repo-{os.urandom(4).hex()}"

            # Prepare workspace creation payload
            create_workspace_dto = {
                "id": workspace_id,
                "name": workspace_id,
                "target": settings.mcp_daytona_target,
                "projects": [{
                    "name": "main",
                    "envVars": env_vars or {},
                    "image": image or "python:3.12-slim",
                    "user": os_user or "root",
                    "source": {
                        "repository": {
                            "id": repo_id,  # Required unique ID
                            "url": "local://workspace",  # Use local URL for sandbox
                            "branch": "main",
                            "name": "sandbox",
                            "owner": "mcp",
                            "sha": "0" * 40,  # 40-character SHA placeholder
                            "source": "local",
                            "path": "/workspace"  # Add workspace path
                        }
                    }
                }]
            }

            print(f"Creating workspace with payload: {json.dumps(create_workspace_dto, indent=2)}")

            async with httpx.AsyncClient(verify=False) as client:
                # Create workspace
                response = await client.post(
                    f"{settings.mcp_daytona_server_url}/workspace",
                    headers={
                        "Authorization": f"Bearer {settings.mcp_daytona_api_key}",
                        "Content-Type": "application/json"
                    },
                    json=create_workspace_dto,
                    timeout=30.0  # Add timeout
                )

                if response.status_code != 200:
                    print(f"Error response: {response.text}")
                response.raise_for_status()
                print(f"Workspace creation response: {response.text}")

                # Start the workspace
                start_response = await client.post(
                    f"{settings.mcp_daytona_server_url}/workspace/{workspace_id}/start",
                    headers={
                        "Authorization": f"Bearer {settings.mcp_daytona_api_key}"
                    },
                    timeout=30.0
                )
                start_response.raise_for_status()
                print(f"Workspace start response: {start_response.text}")

                # Wait for workspace to be ready
                await asyncio.sleep(5)

                return workspace_id

        except Exception as e:
            print(f"\nError creating workspace: {str(e)}")
            if hasattr(e, 'response'):
                print(f"Response: {e.response.text}")
            raise

    @mcp.tool()
    async def execute_claude_code(
        code: str,
        workspace_id: str
    ) -> str:
        """Executes code inside a Daytona workspace."""
        try:
            print(f"Executing code in workspace {workspace_id}")
            async with httpx.AsyncClient(verify=False) as client:
                # First check if workspace is running
                status_response = await client.get(
                    f"{settings.mcp_daytona_server_url}/workspace/{workspace_id}",
                    headers={
                        "Authorization": f"Bearer {settings.mcp_daytona_api_key}"
                    }
                )
                status_response.raise_for_status()

                # Execute the code
                response = await client.post(
                    f"{settings.mcp_daytona_server_url}/workspace/{workspace_id}/main/toolbox/process/execute",
                    headers={
                        "Authorization": f"Bearer {settings.mcp_daytona_api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "command": f"python3 -c '{code}'",
                        "timeout": 30
                    }
                )
                response.raise_for_status()
                result = response.json()

                # Return just the output string
                if isinstance(result, dict):
                    return result.get('result', str(result))
                return str(result)

        except Exception as e:
            print(f"\nError executing code: {str(e)}")
            if hasattr(e, 'response'):
                print(f"Response: {e.response.text}")
            raise

    @mcp.tool()
    async def remove_daytona_env(workspace_id: str) -> str:
        """Removes a Daytona workspace."""
        try:
            async with httpx.AsyncClient(verify=False) as client:
                response = await client.delete(
                    f"{settings.mcp_daytona_server_url}/workspace/{workspace_id}",
                    headers={
                        "Authorization": f"Bearer {settings.mcp_daytona_api_key}"
                    },
                    params={"force": "true"}
                )
                response.raise_for_status()
                return "Workspace removed successfully"

        except Exception as e:
            print(f"\nError removing workspace: {str(e)}")
            if hasattr(e, 'response'):
                print(f"Response: {e.response.text}")
            raise

    return mcp