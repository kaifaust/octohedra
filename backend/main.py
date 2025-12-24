import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import generate

app = FastAPI(title="Octohedra API", version="1.0.0")

# CORS origins - allow localhost for development and production domains
cors_origins = [
    "http://localhost:3001",
    "https://*.vercel.app",
    "https://octohedra.com",
    "https://www.octohedra.com",
]

# Allow additional origins from environment variable
if extra_origins := os.environ.get("CORS_ORIGINS"):
    cors_origins.extend(extra_origins.split(","))

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(generate.router, prefix="/api/v1")


@app.get("/health")
async def health():
    return {"status": "ok"}
