import os
import shutil
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ingestion import extract_text_from_pdf, chunk_text
from retrieval import store_chunks, retrieve_relevant_chunks
from generation import generate_answer

app = FastAPI()

# Allow the React frontend (running on a different port) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://*.vercel.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    text = extract_text_from_pdf(file_path)
    chunks = chunk_text(text)
    doc_id = file.filename.replace(".pdf", "")
    store_chunks(chunks, doc_id=doc_id)

    return {"message": f"Uploaded and processed '{file.filename}'", "chunks_stored": len(chunks)}


class ChatRequest(BaseModel):
    question: str


@app.post("/chat")
async def chat(request: ChatRequest):
    relevant_chunks = retrieve_relevant_chunks(request.question)
    answer = generate_answer(request.question, relevant_chunks)
    return {"answer": answer, "sources": relevant_chunks}