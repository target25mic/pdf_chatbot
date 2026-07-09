import sys
sys.path.append("backend")
from ingestion import extract_text_from_pdf, chunk_text
from retrieval import store_chunks, retrieve_relevant_chunks
from generation import generate_answer

text = extract_text_from_pdf("sample.pdf")
chunks = chunk_text(text)
store_chunks(chunks, doc_id="sample")

question = "What is this document about?"
relevant_chunks = retrieve_relevant_chunks(question)
answer = generate_answer(question, relevant_chunks)

print("Question:", question)
print("Answer:", answer)