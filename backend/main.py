import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers import data, chat, conversations

load_dotenv()


app = FastAPI(
    title="Seoul PM10 AI Assistant API",
    description="서울 미세먼지 데이터를 분석하고 AI 답변을 제공하는 API",
    version="1.0.0",
)

default_origins = (
    "http://127.0.0.1:5500,"
    "http://localhost:5500"
)

allowed_origins = os.getenv(
    "ALLOWED_ORIGINS",
    default_origins
)

origins = [
    origin.strip()
    for origin in allowed_origins.split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(data.router)
app.include_router(chat.router)
app.include_router(conversations.router)


@app.get("/")
def root():
    return {
        "message": "Seoul PM10 AI Assistant API is running."
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }