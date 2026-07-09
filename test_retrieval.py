import sys
sys.path.append("backend")
from ingestion import extract_text_from_pdf, chunk_text
from retrieval import store_chunks, retrieve_relevant_chunks

text = extract_text_from_pdf("sample.pdf")
chunks = chunk_text(text)
store_chunks(chunks, doc_id="sample")

# Change this question to something relevant to your actual PDF's content
results = retrieve_relevant_chunks("What is this document about?")
for i, r in enumerate(results):
    print(f"--- Result {i+1} ---")
    print(r)