import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="ClaimStream API",
    version="0.1.0",
    description="AI-powered multi-agent clinical clarification desk API for hospitals responding to TPA and insurance queries.",
)

# Configure CORS
origins_env = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000")
allowed_origins = [origin.strip() for origin in origins_env.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if allowed_origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    """Health check endpoint for ClaimStream API."""
    return {
        "status": "healthy",
        "service": "ClaimStream API",
    }


@app.get("/")
def root():
    """Root endpoint providing service metadata."""
    return {
        "service": "ClaimStream API",
        "version": "0.1.0",
        "status": "running",
        "docs_url": "/docs",
    }
