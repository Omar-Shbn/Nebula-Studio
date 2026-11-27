from fastapi import APIRouter

from . import chat, ollama

api_router = APIRouter()
api_router.include_router(ollama.router)
api_router.include_router(chat.router)
