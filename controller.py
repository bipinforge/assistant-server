from pathlib import Path
from typing import Iterator

from pydantic import BaseModel
from src.file_service import store_file_details
from src.assistant import init_agent, run_agent
from fastapi import APIRouter, File, UploadFile, Body
from fastapi.responses import StreamingResponse
from src.conversation_history import get_conversation_history, get_conversation_history_by_thread

from src.ingestion_service import query_embedding, ingest_file

router = APIRouter()
UPLOAD_DIR = Path.cwd() / "uploads"

class ChatRequest(BaseModel):
    user_id: str
    model_name: str = "openai:gpt-4o-mini"
    user_message: str = "Hello!"


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    destination = UPLOAD_DIR / file.filename
    with destination.open("wb") as f:
        while chunk := await file.read(1024):
            f.write(chunk)
    file_id = store_file_details(filename=file.filename, filepath=str(destination))
    ingest_file(str(destination))  # Ingest the file after storing its details
    return {"message": f"File uploaded to {destination}", "file_id": file_id}

@router.post("/semantic-search")
async def semantic_search(query: str):
    results = query_embedding(query)
    return {"results": results}

@router.get("/threads")
async def get_threads():
    # Placeholder implementation - replace with actual thread retrieval logic
    threads = get_conversation_history()  # You would implement this to fetch actual threads
    return {"threads": threads}

@router.get("/messages/{thread_id}")
async def get_messages(thread_id: str):
    # Placeholder implementation - replace with actual thread retrieval logic
    conversation = get_conversation_history_by_thread(thread_id)
    return conversation

def _stream_response() -> Iterator[bytes]:
    yield b"Streaming response placeholder.\n"

@router.post("/chat")
def chat_completion(thread_id: str, payload: ChatRequest =  Body(...)):
    strm_res = run_agent(
        thread_id=thread_id,
        user_id=payload.user_id,
        model_name=payload.model_name,
        user_message=payload.user_message,
    )
    return StreamingResponse(strm_res, media_type="text/plain")
