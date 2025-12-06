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
