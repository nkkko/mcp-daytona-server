# mcp-daytona-server

rm -rf .venv
uv venv
source .venv/bin/activate


uv sync --frozen --all-extras --dev


uv run src/main.py