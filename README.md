# Requirements
1. ollama
  - `brew install ollama`
2. python3
  - Recommend `pyenv` or `uv`
  - I used pyenv
3. virtualenv

# Ollama
## Start ollama
- `brew services start ollama`

## Install LLM Model
- `ollama pull <model_name>`
  - [Model list](https://ollama.com/search)

## Run LLM Model
- `ollama run <model_name>`

## Stop ollama
- `brew services stop ollama`

# Python
## Setup Env
1. Setup virtualenv
2. Install dependencies
  - `pip install -r requirements.txt`

# MCP
## Test
### Postman
1. Run MCP Server
2. On Postman
- URL: `http://localhost:8000/mcp`

# Rag
## Pymilvus
- Using milvus-lite to persist and query vector embeddings in local storage

# ReAct (Reasoning + Acting)
- Feedback loop allows agent solve complex, multi-step tasks
- Loop: Observe -> Reason -> Action

# Run Agent and MCP
1. Run LLM model `llama3.1`
  - `ollama run llama3.1`
2. Run History MCP Server
  - `cd mcp`
  - `python3 server.py`
3. Run Math MCP Server
  - `cd examples/fastmcp`
  - `python3 fastmcp_examples.py`
4. Run AI Agent
  - `cd agent`
  - `python3 agent.py`

## Resources
- AI Agent
  - https://medium.com/google-cloud/building-react-agents-from-scratch-a-hands-on-guide-using-gemini-ffe4621d90ae
  - https://www.anthropic.com/engineering/building-effective-agents
