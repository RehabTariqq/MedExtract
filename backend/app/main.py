from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.db.database import check_connection
from app.api.v1.router import api_router
from app.core.exceptions import MedExtractException

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="MedExtract API")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.exception_handler(MedExtractException)
async def medextract_exception_handler(request: Request, exc: MedExtractException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message, "detail": None},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"error": "Invalid request data", "detail": exc.errors()},
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": None},
    )


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "MedExtract API"}


@app.get("/health/db")
async def health_check_db():
    connected = await check_connection()
    if connected:
        return {"status": "ok", "database": "connected"}
    return {"status": "error", "database": "not connected"}