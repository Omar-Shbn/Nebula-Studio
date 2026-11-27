from contextlib import asynccontextmanager

import httpx
from app.routers import api_router
import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config import settings
from app.db import check_database, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    await check_database()
    app.state.ollama = httpx.AsyncClient(
        base_url= settings.OLLAMA_URL,
        timeout=httpx.Timeout(connect=5, read=None, write=30, pool= 5)
    )

    yield


    # -- shutdown --
    await app.state.ollama.aclose()
    await engine.dispose()
app = FastAPI(title=" Nebula Studio", lifespan=lifespan)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(_request: Request, exc: StarletteHTTPException):
    return JSONResponse({"error": exc.detail}, status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_request: Request, exc: RequestValidationError):
    problems = "; ".join(
        f"{'.'.join(str(p) for p in err['loc'][1:]) or 'body'}: {err['msg']}"
        for err in exc.errors()
    )
    return JSONResponse({"error": f"Invalid request: {problems}"}, status_code=422)



app.include_router(api_router, prefix="/api")



if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
