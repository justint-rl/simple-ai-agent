from typing import Dict, List

from fastmcp import FastMCP

from rag import run_rag, search

mcp = FastMCP(name="history")

@mcp.tool
def search_history(search_query: str) -> str:
  return search(search_query)

def run_mcp_server():
  run_rag()
  mcp.run(transport="http")

if __name__ == "__main__":
  run_mcp_server()
