
from fastapi import FastAPI
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
app.include_router(controller_router)
