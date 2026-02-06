from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from .database import Base

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True)
    github_id = Column(Integer, unique=True, nullable=True)
    github_username = Column(String(255), nullable=True)
    display_name = Column(String(255), nullable=True)
    avatar_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    decks = relationship("Deck", back_populates="owner")
    templates = relationship("CardTemplate", back_populates="owner")

class Deck(Base):
    __tablename__ = "decks"
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    artwork_url = Column(String, nullable=True)
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    owner = relationship("User", back_populates="decks")
    cards = relationship("Card", back_populates="deck", cascade="all, delete-orphan")

class CardTemplate(Base):
    __tablename__ = "card_templates"
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    is_default = Column(Boolean, default=False)
    template_json = Column(Text, nullable=True) # Stored as stringified JSON
    preview_image_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    owner = relationship("User", back_populates="templates")

class Card(Base):
    __tablename__ = "cards"
    id = Column(String, primary_key=True, default=generate_uuid)
    deck_id = Column(String, ForeignKey("decks.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Front (visual)
    front_template_id = Column(String, ForeignKey("card_templates.id"), nullable=True)
    front_custom_json = Column(Text, nullable=True)
    front_background_url = Column(String, nullable=True)
    front_title = Column(String(255), nullable=True)
    front_custom_colors = Column(Text, nullable=True)
    
    # Back (content)
    back_content = Column(Text, nullable=True)
    back_format = Column(String, default="markdown")
    
    # Metadata
    tags = Column(Text, nullable=True) # JSON array as string
    is_favorite = Column(Boolean, default=False)
    
    # Embeddings
    content_embedding = Column(Text, nullable=True) # JSON array as string
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    deck = relationship("Deck", back_populates="cards")

class GitHubExport(Base):
    __tablename__ = "github_exports"
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    deck_id = Column(String, ForeignKey("decks.id", ondelete="CASCADE"), nullable=False)
    github_repo_url = Column(String, nullable=True)
    last_exported_at = Column(DateTime(timezone=True), nullable=True)
    last_synced_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
