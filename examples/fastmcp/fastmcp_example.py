from fastmcp import FastMCP

mcp = FastMCP(name="math")

@mcp.tool
def add(a: int, b: int) -> int:
  return a + b

def run_mcp_server():
  mcp.run(transport="http", port=8001)

if __name__ == "__main__":
  run_mcp_server()
