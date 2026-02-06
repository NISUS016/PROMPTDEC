"""
PromptDec Backend - FastAPI Application
Phase 1B: Backend Core
"""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
from typing import List

from .database import engine, Base, get_db
from . import models, schemas

# Load environment variables
load_dotenv()

# Create tables (SQLite/Local only - in production use migrations)
models.Base.metadata.create_all(bind=engine)

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

# --- PLACEHOLDER FOR AUTH ---
TEST_USER_ID = "test-user-123"

def ensure_test_user(db: Session):
    user = db.query(models.User).filter(models.User.id == TEST_USER_ID).first()
    if not user:
        user = models.User(id=TEST_USER_ID, display_name="Test User")
        db.add(user)
        db.commit()
    return user

# --- END AUTH PLACEHOLDER ---

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

# --- DECKS ENDPOINTS ---

@app.get("/decks", response_model=List[schemas.DeckResponse])
async def get_decks(db: Session = Depends(get_db)):
    ensure_test_user(db)
    return db.query(models.Deck).filter(models.Deck.user_id == TEST_USER_ID).all()

@app.post("/decks", response_model=schemas.DeckResponse)
async def create_deck(deck: schemas.DeckCreate, db: Session = Depends(get_db)):
    ensure_test_user(db)
    db_deck = models.Deck(**deck.model_dump(), user_id=TEST_USER_ID)
    db.add(db_deck)
    db.commit()
    db.refresh(db_deck)
    return db_deck

@app.get("/decks/{deck_id}", response_model=schemas.DeckResponse)
async def get_deck(deck_id: str, db: Session = Depends(get_db)):
    deck = db.query(models.Deck).filter(models.Deck.id == deck_id, models.Deck.user_id == TEST_USER_ID).first()
    if not deck:
        raise HTTPException(status_code=404, detail="Deck not found")
    return deck

# Application startup event
@app.on_event("startup")
async def startup_event():
    """Execute on application startup"""
    print("🚀 PromptDec API starting up...")
    print(f"📍 CORS origins: {origins}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )