"""
PromptDec Backend - FastAPI Application
Phase 1B: Backend Core
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="PromptDec API",
    description="Backend API for PromptDec prompt gallery",
    version="0.1.0",
)

# CORS Configuration
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health Check Endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint to verify API is running"""
    return {
        "status": "healthy",
        "service": "promptdec-api",
        "version": "0.1.0"
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "PromptDec API",
        "docs": "/docs",
        "health": "/health"
    }


# Application startup event
@app.on_event("startup")
async def startup_event():
    """Execute on application startup"""
    print("🚀 PromptDec API starting up...")
    print(f"📍 CORS origins: {origins}")


# Application shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Execute on application shutdown"""
    print("👋 PromptDec API shutting down...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
