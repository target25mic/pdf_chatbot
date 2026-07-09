import sys
sys.path.append("backend")
from ingestion import extract_text_from_pdf, chunk_text


text = extract_text_from_pdf("sample.pdf")
chunks = chunk_text(text)
print(f"Total chunks: {len(chunks)}")
print("--- Chunk 1 ---")
print(chunks[0])
print("--- Chunk 2 ---")
print(chunks[1])