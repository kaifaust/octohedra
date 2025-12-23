from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import generate

app = FastAPI(title="Octoflake API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3001",
        "https://*.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(generate.router, prefix="/api/v1")


@app.get("/health")
async def health():
    return {"status": "ok"}
