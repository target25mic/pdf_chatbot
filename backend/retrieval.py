import os
import chromadb
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")  # small, fast, free, local

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="pdf_chunks")

def get_embedding(text: str) -> list[float]:
    return embedding_model.encode(text).tolist()

def store_chunks(chunks: list[str], doc_id: str):
    for i, chunk in enumerate(chunks):
        embedding = get_embedding(chunk)
        collection.add(
            ids=[f"{doc_id}_chunk_{i}"],
            embeddings=[embedding],
            documents=[chunk],
            metadatas=[{"doc_id": doc_id, "chunk_index": i}]
        )
    print(f"Stored {len(chunks)} chunks for doc '{doc_id}'")

def retrieve_relevant_chunks(query: str, top_k: int = 4) -> list[str]:
    query_embedding = get_embedding(query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    return results["documents"][0]