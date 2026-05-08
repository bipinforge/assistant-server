
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controller import router as controller_router
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from src.assistant import init_agent


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()
    init_agent()

    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(controller_router)
