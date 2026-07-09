import os
import chromadb
import cohere
from dotenv import load_dotenv

load_dotenv()
co = cohere.Client(os.getenv("COHERE_API_KEY"))

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="pdf_chunks")

def get_embedding(text: str, input_type: str = "search_document") -> list[float]:
    response = co.embed(
        texts=[text],
        model="embed-english-v3.0",
        input_type=input_type
    )
    return response.embeddings[0]

def store_chunks(chunks: list[str], doc_id: str):
    for i, chunk in enumerate(chunks):
        embedding = get_embedding(chunk, input_type="search_document")
        collection.add(
            ids=[f"{doc_id}_chunk_{i}"],
            embeddings=[embedding],
            documents=[chunk],
            metadatas=[{"doc_id": doc_id, "chunk_index": i}]
        )
    print(f"Stored {len(chunks)} chunks for doc '{doc_id}'")

def retrieve_relevant_chunks(query: str, top_k: int = 4) -> list[str]:
    query_embedding = get_embedding(query, input_type="search_query")
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    return results["documents"][0]