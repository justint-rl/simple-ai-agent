from pathlib import Path

import numpy as np
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

def run_rag():
  collection_name = "demo_collection"
  embedding_generator = EmbeddingGenerator()
  # Create collection
  if not client.has_collection(collection_name):
    client.create_collection(
      collection_name=collection_name,
      dimension=_DIMENSION,
    )
    print(f"Created collection {collection_name}")
  else:
    print(f"Collection already created {collection_name}")

  # Generate embeddings
  docs = [
    "AI was founded as an academic discipline in 1956.",
    "Alan Turing was the first person to conduct substantial research in AI",
    "Born in Maida Vale, London, Turing was raised in southern England.",
    "Percy Jackson is a half-blood son of zeus"
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
    collection_name=collection_name,
    data=data,
  )

  # Query embeddings
  search_query = "who is related to zeus?"
  search_embedding = embedding_generator.generate_embedding(search_query)
  res = client.search(
    collection_name=collection_name,
    data=[search_embedding],
    limit=1,
    output_fields=["id", "text"],
  )
  print(res)

  # Drop collection
  client.drop_collection(collection_name=collection_name)

if __name__ == "__main__":
  run_rag()
