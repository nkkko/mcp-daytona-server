# src/mcp_daytona_server/inspect_sdk.py
import inspect
from daytona_sdk import Daytona, CreateWorkspaceParams

def inspect_sdk():
    print("\nInspecting Daytona SDK:")

    print("\nDaytona class methods:")
    for name, member in inspect.getmembers(Daytona):
        if not name.startswith('_'):  # Skip private methods
            print(f"- {name}: {member}")

    print("\nCreateWorkspaceParams accepted arguments:")
    print(inspect.signature(CreateWorkspaceParams))

if __name__ == "__main__":
    inspect_sdk()