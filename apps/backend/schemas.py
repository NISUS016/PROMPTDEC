from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    id: str
    github_username: Optional[str] = None
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None

class UserResponse(UserBase):
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# --- Decks ---

class DeckBase(BaseModel):
    name: str
    description: Optional[str] = None
    artwork_url: Optional[str] = None
    is_public: bool = False

class DeckCreate(DeckBase):
    pass

class DeckUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    artwork_url: Optional[str] = None
    is_public: Optional[bool] = None

class DeckResponse(DeckBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

# --- Cards ---

class CardBase(BaseModel):
    deck_id: str
    front_template_id: Optional[str] = None
    front_title: Optional[str] = None
    front_custom_json: Optional[str] = None
    front_background_url: Optional[str] = None
    front_custom_colors: Optional[str] = None
    back_content: Optional[str] = None
    back_format: str = "markdown"
    tags: Optional[str] = None # JSON array as string
    is_favorite: bool = False
    content_embedding: Optional[str] = None # JSON array as string

class CardCreate(CardBase):
    pass

class CardUpdate(BaseModel):
    deck_id: Optional[str] = None
    front_template_id: Optional[str] = None
    front_title: Optional[str] = None
    front_custom_json: Optional[str] = None
    front_background_url: Optional[str] = None
    front_custom_colors: Optional[str] = None
    back_content: Optional[str] = None
    back_format: Optional[str] = None
    tags: Optional[str] = None
    is_favorite: Optional[bool] = None
    content_embedding: Optional[str] = None

class CardResponse(CardBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)