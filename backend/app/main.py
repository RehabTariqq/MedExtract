from fastapi import FastAPI
from app.db.database import check_connection

app = FastAPI(title="MedExtract API")


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "MedExtract API"}


@app.get("/health/db")
async def health_check_db():
    connected = await check_connection()
    if connected:
        return {"status": "ok", "database": "connected"}
    return {"status": "error", "database": "not connected"}