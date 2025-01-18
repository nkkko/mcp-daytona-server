# mcp-daytona-server

# CLEANUP AND INSTALL
```bash
rm -rf .venv
uv venv
source .venv/bin/activate
uv sync --frozen --all-extras --dev
```

# RUN SERVER
```bash
PYTHONPATH=$PYTHONPATH:$(pwd)/src uv run src/mcp_daytona_server/main.py
```

# RUN TEST
 ```bash
 PYTHONPATH=$PYTHONPATH:$(pwd)/src uv run src/mcp_daytona_server/test_client.py
 PYTHONPATH=$PYTHONPATH:$(pwd)/src uv run src/mcp_daytona_server/list_configs.py
 ```