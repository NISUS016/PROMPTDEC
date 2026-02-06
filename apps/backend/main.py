"""
PromptDec Backend - FastAPI Application
Phase 1B: Backend Core - Complete CRUD
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
from typing import List, Optional

from database import engine, Base, get_db
import models, schemas

# Load environment variables
load_dotenv()

# Create tables
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

# Health Check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "promptdec-api", "version": "0.1.0"}

@app.get("/")
async def root():
    return {"message": "PromptDec API", "docs": "/docs", "health": "/health"}

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

@app.put("/decks/{deck_id}", response_model=schemas.DeckResponse)
async def update_deck(deck_id: str, deck_update: schemas.DeckUpdate, db: Session = Depends(get_db)):
    db_deck = db.query(models.Deck).filter(models.Deck.id == deck_id, models.Deck.user_id == TEST_USER_ID).first()
    if not db_deck:
        raise HTTPException(status_code=404, detail="Deck not found")
    
    update_data = deck_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_deck, key, value)
    
    db.commit()
    db.refresh(db_deck)
    return db_deck

@app.delete("/decks/{deck_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_deck(deck_id: str, db: Session = Depends(get_db)):
    db_deck = db.query(models.Deck).filter(models.Deck.id == deck_id, models.Deck.user_id == TEST_USER_ID).first()
    if not db_deck:
        raise HTTPException(status_code=404, detail="Deck not found")
    
    db.delete(db_deck)
    db.commit()
    return None

# --- CARDS ENDPOINTS ---

@app.get("/cards", response_model=List[schemas.CardResponse])
async def get_cards(deck_id: Optional[str] = None, db: Session = Depends(get_db)):
    ensure_test_user(db)
    query = db.query(models.Card).filter(models.Card.user_id == TEST_USER_ID)
    if deck_id:
        query = query.filter(models.Card.deck_id == deck_id)
    return query.all()

@app.post("/cards", response_model=schemas.CardResponse)
async def create_card(card: schemas.CardCreate, db: Session = Depends(get_db)):
    ensure_test_user(db)
    # Verify deck exists and belongs to user
    deck = db.query(models.Deck).filter(models.Deck.id == card.deck_id, models.Deck.user_id == TEST_USER_ID).first()
    if not deck:
        raise HTTPException(status_code=400, detail="Invalid deck_id")
    
    db_card = models.Card(**card.model_dump(), user_id=TEST_USER_ID)
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card

@app.get("/cards/{card_id}", response_model=schemas.CardResponse)
async def get_card(card_id: str, db: Session = Depends(get_db)):
    card = db.query(models.Card).filter(models.Card.id == card_id, models.Card.user_id == TEST_USER_ID).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    return card

@app.put("/cards/{card_id}", response_model=schemas.CardResponse)
async def update_card(card_id: str, card_update: schemas.CardUpdate, db: Session = Depends(get_db)):
    db_card = db.query(models.Card).filter(models.Card.id == card_id, models.Card.user_id == TEST_USER_ID).first()
    if not db_card:
        raise HTTPException(status_code=404, detail="Card not found")
    
    update_data = card_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_card, key, value)
    
    db.commit()
    db.refresh(db_card)
    return db_card

@app.delete("/cards/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_card(card_id: str, db: Session = Depends(get_db)):
    db_card = db.query(models.Card).filter(models.Card.id == card_id, models.Card.user_id == TEST_USER_ID).first()
    if not db_card:
        raise HTTPException(status_code=404, detail="Card not found")
    
    db.delete(db_card)
    db.commit()
    return None

@app.post("/cards/{card_id}/duplicate", response_model=schemas.CardResponse)
async def duplicate_card(card_id: str, db: Session = Depends(get_db)):
    db_card = db.query(models.Card).filter(models.Card.id == card_id, models.Card.user_id == TEST_USER_ID).first()
    if not db_card:
        raise HTTPException(status_code=404, detail="Card not found")
    
    # Create new card with same attributes but new ID
    card_data = {c.name: getattr(db_card, c.name) for c in models.Card.__table__.columns if c.name not in ['id', 'created_at', 'updated_at']}
    new_card = models.Card(**card_data)
    new_card.front_title = f"{new_card.front_title} (Copy)"
    
    db.add(new_card)
    db.commit()
    db.refresh(new_card)
    return new_card

# Startup and Shutdown
@app.on_event("startup")
async def startup_event():
    print("🚀 PromptDec API starting up...")

if __name__ == "__main__":
    import uvicorn
    from typing import Optional
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
