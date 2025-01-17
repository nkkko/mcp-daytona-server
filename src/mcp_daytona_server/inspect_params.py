# src/mcp_daytona_server/inspect_params.py
from daytona_sdk import CreateWorkspaceParams
import inspect

def inspect_params():
    print("\nInspecting CreateWorkspaceParams:")
    print("\nClass signature:")
    print(inspect.signature(CreateWorkspaceParams))

    print("\nClass fields:")
    for name, field in CreateWorkspaceParams.__fields__.items():
        print(f"\n{name}:")
        print(f"  type: {field.type_}")
        print(f"  required: {field.required}")
        print(f"  default: {field.default}")
        if field.description:
            print(f"  description: {field.description}")

if __name__ == "__main__":
    inspect_params()