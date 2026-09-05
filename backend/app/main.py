from fastapi import FastAPI

app = FastAPI(title="MedExtract API")


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "MedExtract API"}