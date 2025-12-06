import asyncio
import json
from typing import Dict

from fastmcp import Client as MCPClient
import ollama

_DEFAULT_LLM_MODEL = "llama3.1"

_SYSTEM_PROMPT = """
You are a helpful historian and mathematician assistant with access to various tools.

Your capabilities include:
- Querying local knowledge base (RAG) for specific information
- Use RAG for math operation

When given a task:
1. Think step-by-step about what need to do
2. Use tools to gather information or make changes
3. Observe results and continue until the task is complete
4. Explain what you did step-by-step

Guidelines:
- Use knowledge base for specific information about history
- Use tool to do mathematical operations
- Do not use any information outside of the tools provided to you
"""

class MCPAgent:
  def __init__(self, model: str = _DEFAULT_LLM_MODEL, mcp_servers: Dict[str, str] = {}):
    self._model = model
    self._mcp_servers = mcp_servers
    self._conversation_history = []
    self._tools = []
    self._tools_to_mcp_client = {}
    self._mcp_clients = {}

  async def connect_mcp_servers(self):
    """
    Connect to all MCP servers
    """
    for name, host in self._mcp_servers.items():
      print(f"Connecting to {name} at {host}")
      try:
        mcp_client = MCPClient(host)
        await mcp_client.__aenter__()
        tools = await mcp_client.list_tools()
        for tool in tools:
          self._tools.append({
            "type": "function",
            "function": {
              "name": tool.name,
              "description": tool.description or "",
              "parameters": tool.inputSchema or {"type": "object", "properties": {}},
            }
          })
          self._tools_to_mcp_client[tool.name] = mcp_client
        self._mcp_clients[name] = mcp_client
        print(f"Connected to {name} MCP: {len(tools)} tools")
      except Exception as e:
        print(e)
    print(f"Connected to all MCP servers. Total tools available: {self._tools}")

  async def _call_tool(self, tool_name: str, args: Dict) -> str:
    mcp_client = self._tools_to_mcp_client[tool_name]
    result = await mcp_client.call_tool(tool_name, args)
    if result and result.content:
      texts = []
      for item in result.content:
        if hasattr(item, "text"):
          texts.append(item.text)
      return '\n'.join(texts) if texts else "(no output)"
    return "(no output)"

  async def run(self, user_message: str) -> str:
    self._conversation_history.append({
      "role": "user",
      "content": user_message
    })

    curr_loop = 0
    max_loop = 10
    while curr_loop < max_loop:
      response = ollama.chat(
        model=_DEFAULT_LLM_MODEL,
        messages=[
          {"role": "system", "content": _SYSTEM_PROMPT},
          *self._conversation_history,
        ],
        tools=self._tools,
      )
      print(response)
      message = response["message"]
      content = message.get("content", "")
      tool_calls = message.get("tool_calls", [])
      if tool_calls:
        self._conversation_history.append({
          "role": "assistant",
          "content": content,
          "tool_calls": tool_calls,
        })
        # Process tool call
        for tool_call in tool_calls:
          tool_name = tool_call.function.name
          tool_args = tool_call.function.arguments
          if isinstance(tool_args, str):
            try:
              tool_args = json.loads(tool_args)
            except json.decoder.JSONDecodeError:
              tool_args = {}
          print(f"{tool_name}({tool_args})")
          result = await self._call_tool(tool_name, tool_args)
          if len(result) > 5000:
            result = result[:5000] + "\n... (truncated)"
          self._conversation_history.append({
            "role": "tool",
            "content": result,
          })
        curr_loop += 1
      else:
        self._conversation_history.append({
          "role": "assistant",
          "content": content,
        })
        return content

async def main():
  mcp_servers = {
    "math": "http://localhost:8001/mcp",
    "rag": "http://localhost:8000/mcp",
  }
  agent = MCPAgent(mcp_servers=mcp_servers)
  print("=" * 60)
  print("FastMCP Coding Agent")
  print("=" * 60)
  print("Commands: 'quit' to exit, 'clear' to reset conversation")
  print("=" * 60)
  print()

  await agent.connect_mcp_servers()

  while True:
    try:
      user_input = input("You: ").strip()
    except (EOFError, KeyboardInterrupt):
      print("\nGoodbye!")
      break

    if not user_input:
      continue

    if user_input.lower() == 'quit':
      print("Goodbye!")
      break

    print("\nAgent:", flush=True)
    response = await agent.run(user_input)
    print()
    print(response)
    print()

if __name__ == '__main__':
  asyncio.run(main())

