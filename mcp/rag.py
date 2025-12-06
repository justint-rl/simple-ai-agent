from pathlib import Path
from typing import Dict, List

from numpy import ndarray
from pymilvus import MilvusClient
from sentence_transformers import SentenceTransformer

_llm_embedding_model = "all-MiniLM-L6-v2"

class EmbeddingGenerator:
  def __init__(self, llm_embedding_model: str = _llm_embedding_model):
    self._model = SentenceTransformer(llm_embedding_model)

  def generate_embedding(self, text: str) -> ndarray:
    return self._model.encode(text)

_DB_PATH = Path(__file__).parent / "db"
client = MilvusClient(f"{_DB_PATH}/milvus_demo.db")

_DIMENSION = 384
_COLLECTION_NAME = "demo_collection"

def search(search_query: str) -> str:
  embedding_generator = EmbeddingGenerator()
  search_embedding = embedding_generator.generate_embedding(search_query)
  res = client.search(
    collection_name=_COLLECTION_NAME,
    data=[search_embedding],
    limit=1,
    output_fields=["id", "text"],
  )
  output = []
  print(res)
  for i, hit in enumerate(res[0]):
    distance = hit.get("distance", 0)
    entity = hit.get("entity", {})
    text = entity.get("text", "")
    output.append(f"--- Result {i} (similarity: {distance:.3f} ---")
    doc_preview = text[:500] + "..." if len(text) > 500 else text
    output.append(doc_preview)
  return '\n'.join(output)

def run_rag():
  embedding_generator = EmbeddingGenerator()
  # Create collection
  if not client.has_collection(_COLLECTION_NAME):
    client.create_collection(
      collection_name=_COLLECTION_NAME,
      dimension=_DIMENSION,
    )
    print(f"Created collection {_COLLECTION_NAME}")
  else:
    print(f"Collection already created {_COLLECTION_NAME}")

  # Generate embeddings
  docs = [
    "AI was founded as an academic discipline in 1956.",
    "Alan Turing was the first person to conduct substantial research in AI",
    "Born in Maida Vale, London, Turing was raised in southern England.",
    "Percy Jackson is a half-blood son of zeus",
    "cake was invented by mr cakeman"
  ]
  vectors = [
    embedding_generator.generate_embedding(d)
    for d in docs
  ]
  data = [
    {"id": i, "text": docs[i], "vector": vectors[i].tolist()}
    for i in range(len(vectors))
  ]

  # Add embeddings to DB
  res = client.insert(
    collection_name=_COLLECTION_NAME,
    data=data,
  )

  # # Query embeddings
  # search_query = "who is related to zeus?"
  # search_embedding = embedding_generator.generate_embedding(search_query)
  # res = client.search(
  #   collection_name=_COLLECTION_NAME,
  #   data=[search_embedding],
  #   limit=1,
  #   output_fields=["id", "text"],
  # )
  # print(res)
  #
  # # Drop collection
  # client.drop_collection(collection_name=_COLLECTION_NAME)

if __name__ == "__main__":
  run_rag()
