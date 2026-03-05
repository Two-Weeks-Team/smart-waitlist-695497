from fastapi import FastAPI
from routes import router

app = FastAPI(title="Smart Waitlist API", version="1.0.0")

app.include_router(router, prefix="/api/v1")


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "smart-waitlist-api"
    }
