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

class DeckBase(BaseModel):
    name: str
    description: Optional[str] = None
    artwork_url: Optional[str] = None
    is_public: bool = False

class DeckCreate(DeckBase):
    pass

class DeckResponse(DeckBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class CardBase(BaseModel):
    deck_id: str
    front_template_id: Optional[str] = None
    front_title: Optional[str] = None
    back_content: Optional[str] = None
    tags: Optional[str] = None # Expecting stringified JSON or CSV
    is_favorite: bool = False

class CardCreate(CardBase):
    pass

class CardResponse(CardBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
