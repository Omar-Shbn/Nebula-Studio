import httpx
from fastapi import Request


def get_ollama_client(request: Request) -> httpx.AsyncClient:
    """The shared httpx client created in the lifespan."""
    return request.app.state.ollama
