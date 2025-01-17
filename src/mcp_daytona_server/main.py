# src/mcp_daytona_server/main.py
from mcp_daytona_server.mcp_server import create_mcp_server

def main():
    mcp = create_mcp_server()
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()