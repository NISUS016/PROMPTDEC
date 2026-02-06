# PromptDec - Architecture Document

## 1. Project Overview

**PromptDec** is a personal prompt gallery application styled as a trading card game (TCG). It allows users to organize, search, and customize prompt cards across multiple decks. The app features semantic search, card flip animations, GitHub integration for sharing, and dual deployment targets (web and desktop).

**Core Value Proposition:**
- Semantic/vector search to find prompts by context, not exact keywords
- TCG-style card flip interactions with customizable card designs
- Multi-deck organization (decks as folders, cards as notes)
- Markdown support for prompt content
- Cross-platform (web + desktop) with GitHub as interchange format

**User Personas:**
1. Power users maintaining personal prompt libraries
2. Developers/designers needing quick prompt access
3. Community members discovering shared prompt decks on GitHub

---

## 2. Deployment Strategy & Phases

### Phase 1: Web Version (Priority)
- **Platform:** Vercel
- **Target Users:** GitHub users wanting cloud-based prompt management
- **Storage:** Supabase (PostgreSQL + file storage)
- **Auth:** GitHub OAuth
- **Sync Strategy:** Auto-sync on create/delete, manual save on edit

### Phase 2: Desktop Version (Post-launch)
- **Platform:** Tauri
- **Target Users:** Users wanting offline-first, local-only prompts
- **Storage:** SQLite (local) + optional JSON export
- **Auth:** None required
- **Sync Strategy:** Manual save for all operations, manual GitHub push
- **File Format:** JSON export for GitHub interchange

### Cross-platform Considerations
- GitHub acts as universal interchange format
- Web users can export decks → GitHub → Desktop users can import
- Desktop users can push decks → GitHub → Web users can pull/sync
- Data model remains consistent across platforms

---

## 3. Tech Stack

### Frontend (Web)
- **Framework:** React 18+ (Vite)
- **Styling:** Tailwind CSS
- **UI Components:** Shadcn/UI
- **State Management:** React Query (TanStack Query) for server state, Zustand for client state
- **Animation:** Framer Motion (for 3D flip, hover effects)
- **Search:** Integration with backend semantic search API
- **File Upload:** React-Dropzone for drag-and-drop
- **Markdown:** react-markdown + remark-gfm for rendering

### Frontend (Desktop)
- **Framework:** Tauri + React (same as web)
- **File Access:** Tauri's file system API
- **Local Storage:** SQLite via sql.js or better-sqlite3
- **Styling:** Same (Tailwind + Shadcn)

### Backend
- **Framework:** FastAPI (Python)
- **Database:** PostgreSQL (via Supabase)
- **ORM:** SQLAlchemy
- **Authentication:** GitHub OAuth (Supabase Auth)
- **Vector Search:** pgvector + Supabase Vector (for semantic search)
- **File Storage:** Supabase Storage (AWS S3-backed)
- **API Documentation:** FastAPI Swagger/OpenAPI

### Database
- **Primary:** Supabase (PostgreSQL)
- **Vector Embeddings:** pgvector extension
- **File Storage:** Supabase Storage buckets
- **Real-time Sync:** Supabase Realtime (optional for web)

### DevOps
- **Web Deployment:** Vercel (auto-deploy from GitHub)
- **Backend Deployment:** Railway or Render (Python/FastAPI)
- **Database:** Supabase Postgres
- **File Storage:** Supabase Storage
- **Version Control:** GitHub

### Authentication & Authorization
- **Web:** GitHub OAuth via Supabase Auth
- **Desktop:** None (local development mode)
- **Token Storage:** Browser localStorage (web), secure storage (Tauri)

---

## 4. Data Models & Database Schema

### Core Entities

#### User
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY (Supabase Auth),
  github_username VARCHAR UNIQUE,
  github_id INTEGER UNIQUE,
  display_name VARCHAR,
  avatar_url TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

#### Deck (Case of Cards)
```sql
CREATE TABLE decks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  name VARCHAR NOT NULL,
  description TEXT,
  artwork_url TEXT (URL to card case art),
  is_public BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(user_id, name)
);
```

#### Card
```sql
CREATE TABLE cards (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  deck_id UUID NOT NULL REFERENCES decks(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  
  -- Front (visual)
  front_template_id UUID REFERENCES card_templates(id),
  front_custom_json JSONB (custom front data if using custom template),
  front_background_url TEXT (image URL),
  front_title VARCHAR,
  front_custom_colors JSONB (color palette),
  
  -- Back (content)
  back_content TEXT (markdown),
  back_format VARCHAR DEFAULT 'markdown' ('markdown' | 'txt'),
  
  -- Metadata
  tags TEXT[] (array of tags),
  is_favorite BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  
  -- For semantic search
  content_embedding vector(1536) (OpenAI embeddings)
);

CREATE INDEX ON cards USING IVFFLAT (content_embedding vector_cosine_ops);
```

#### Card Template
```sql
CREATE TABLE card_templates (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  name VARCHAR NOT NULL,
  description TEXT,
  is_default BOOLEAN DEFAULT FALSE,
  is_custom BOOLEAN DEFAULT FALSE,
  
  -- Template definition
  template_json JSONB (schema defining zones, styling),
  preview_image_url TEXT,
  
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  
  UNIQUE(user_id, name)
);
```

#### Default Templates (seeded)
```sql
-- Pokémon-style
-- Modern art-style
-- Minimalist
-- MTG-style
-- Custom (user-created)
```

#### Tags
```sql
CREATE TABLE tags (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  name VARCHAR NOT NULL,
  color VARCHAR DEFAULT '#808080',
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(user_id, name)
);
```

#### GitHub Export Log (for tracking syncs)
```sql
CREATE TABLE github_exports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  deck_id UUID NOT NULL REFERENCES decks(id),
  github_repo_url VARCHAR,
  last_exported_at TIMESTAMP,
  last_synced_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 5. Component Architecture

### Folder Structure (Frontend)

```
src/
├── components/
│   ├── Layout/
│   │   ├── Navbar.tsx (top bar with search, branding, nav)
│   │   ├── Sidebar.tsx (left sidebar with deck nav)
│   │   └── MainLayout.tsx (wrapper for layout)
│   │
│   ├── HomePage/
│   │   ├── DeckGrid.tsx (grid of deck cases)
│   │   ├── DeckCard.tsx (individual deck case with artwork)
│   │   └── CreateDeckButton.tsx
│   │
│   ├── DeckView/
│   │   ├── CardGrid.tsx (grid of cards)
│   │   ├── CardList.tsx (list view with preview)
│   │   ├── ViewToggle.tsx (grid/list switch)
│   │   ├── CardThumbnail.tsx (card preview)
│   │   └── CreateCardButton.tsx
│   │
│   ├── CardView/
│   │   ├── CardFlip.tsx (3D flip container with Framer Motion)
│   │   ├── CardFront.tsx (renders template + customization)
│   │   ├── CardBack.tsx (renders markdown content)
│   │   ├── CardActions.tsx (copy, edit, delete, favorite, tag)
│   │   └── CardEditor.tsx (edit mode interface)
│   │
│   ├── CardBuilder/
│   │   ├── CardBuilderModal.tsx (main builder)
│   │   ├── TemplateSelector.tsx (choose template)
│   │   ├── FrontCustomizer.tsx (background, colors, etc.)
│   │   ├── BackEditor.tsx (markdown/txt editor)
│   │   ├── FileUploadZone.tsx (drag-drop background)
│   │   ├── ReactImporter.tsx (import custom React component)
│   │   ├── LivePreview.tsx (split preview pane)
│   │   └── TagEditor.tsx
│   │
│   ├── Search/
│   │   ├── SemanticSearchBar.tsx (center top, animates)
│   │   └── SearchResults.tsx
│   │
│   ├── Sidebar/
│   │   ├── DeckList.tsx
│   │   ├── RecentDecks.tsx
│   │   ├── FavoritesFilter.tsx
│   │   ├── TagBrowser.tsx
│   │   └── SettingsMenu.tsx
│   │
│   ├── Common/
│   │   ├── FloatingActionButton.tsx
│   │   ├── Modal.tsx
│   │   ├── LoadingSpinner.tsx
│   │   └── Toast.tsx
│   │
│   └── GitHubIntegration/
│       ├── ExportModal.tsx
│       ├── SyncStatus.tsx
│       └── ImportFromGitHub.tsx
│
├── hooks/
│   ├── useDecks.ts (TanStack Query for decks)
│   ├── useCards.ts (TanStack Query for cards)
│   ├── useSemanticSearch.ts
│   ├── useCardBuilder.ts (builder state)
│   ├── useKeyboardShortcuts.ts (Cmd+N logic)
│   └── useGitHubSync.ts
│
├── stores/
│   ├── uiStore.ts (Zustand - UI state)
│   ├── authStore.ts (current user)
│   └── builderStore.ts (card builder state)
│
├── api/
│   ├── client.ts (fetch wrapper)
│   ├── decks.ts (deck endpoints)
│   ├── cards.ts (card endpoints)
│   ├── search.ts (semantic search)
│   ├── templates.ts (template endpoints)
│   ├── github.ts (GitHub OAuth + sync)
│   └── auth.ts (Supabase Auth)
│
├── utils/
│   ├── markdown.ts (markdown parsing)
│   ├── cardRenderer.ts (template → React component)
│   ├── embeddings.ts (vector embedding client)
│   ├── fileStorage.ts (Supabase storage)
│   └── validators.ts
│
├── types/
│   ├── index.ts (TypeScript interfaces)
│   └── api.ts (API response types)
│
├── styles/
│   ├── globals.css
│   ├── cards.css (flip animation, card styles)
│   └── layout.css
│
├── App.tsx
├── main.tsx
└── index.css
```

### Component Hierarchy (High-level)

```
App
├── AuthGuard (GitHub OAuth)
├── MainLayout
│   ├── Navbar
│   │   ├── Logo/Branding
│   │   ├── SemanticSearchBar
│   │   └── UserMenu
│   ├── Sidebar
│   │   ├── DeckList
│   │   ├── RecentDecks
│   │   ├── FavoritesFilter
│   │   └── TagBrowser
│   └── MainContent
│       ├── HomePage
│       │   └── DeckGrid
│       │       └── DeckCard[]
│       ├── DeckView
│       │   ├── ViewToggle (grid/list)
│       │   ├── CardGrid / CardList
│       │   │   └── CardThumbnail[] / CardListItem[]
│       │   └── FloatingActionButton (create card)
│       └── CardView
│           ├── CardFlip
│           │   ├── CardFront (template renderer)
│           │   └── CardBack (markdown renderer)
│           └── CardActions
├── CardBuilderModal
│   ├── TemplateSelector
│   ├── FrontCustomizer
│   │   ├── FileUploadZone
│   │   ├── ColorPicker
│   │   └── ReactImporter
│   ├── BackEditor
│   ├── LivePreview
│   └── TagEditor
└── Modals & Overlays
    ├── ConfirmDelete
    ├── ExportToGitHub
    └── ImportFromGitHub
```

---

## 6. API Endpoints (Backend)

### Authentication
```
POST /auth/github/callback
  - Exchange GitHub code for Supabase session
  - Returns: auth token, user profile

GET /auth/me
  - Get current authenticated user
  - Returns: User object
```

### Decks
```
GET /decks
  - List all decks for authenticated user
  - Query: ?search=, ?limit=10, ?offset=0
  - Returns: Deck[]

POST /decks
  - Create new deck
  - Body: { name, description, artwork_url? }
  - Returns: Deck

GET /decks/{deckId}
  - Get single deck with card count
  - Returns: Deck + metadata

PUT /decks/{deckId}
  - Update deck (name, description, artwork)
  - Body: { name?, description?, artwork_url? }
  - Returns: Deck

DELETE /decks/{deckId}
  - Delete deck and all cards
  - Returns: { success: true }
```

### Cards
```
GET /decks/{deckId}/cards
  - List cards in deck
  - Query: ?search=, ?tag=, ?favorite=true, ?limit=20, ?offset=0
  - Returns: Card[]

POST /decks/{deckId}/cards
  - Create new card
  - Body: { 
      front_template_id?, front_custom_json?, front_background_url?,
      front_title?, front_custom_colors?,
      back_content, back_format,
      tags?
    }
  - On create: Automatically generate embedding + sync to web
  - Returns: Card

GET /cards/{cardId}
  - Get single card
  - Returns: Card

PUT /cards/{cardId}
  - Update card (called on manual save)
  - Body: { back_content?, front_custom_json?, tags?, is_favorite? }
  - On save: Regenerate embedding + sync to web
  - Returns: Card

DELETE /cards/{cardId}
  - Delete card
  - Returns: { success: true }

POST /cards/{cardId}/duplicate
  - Duplicate card to same or different deck
  - Body: { target_deck_id }
  - Returns: Card
```

### Semantic Search
```
POST /search/semantic
  - Vector search across all cards
  - Query scope: ?deck_id= (specific deck) or all decks
  - Body: { query, limit=10, threshold=0.7 }
  - Process:
    1. Embed user query using OpenAI embeddings API
    2. pgvector cosine similarity search
    3. Return top K matches
  - Returns: Card[] (sorted by relevance)
```

### Templates
```
GET /templates
  - List all available templates (default + user custom)
  - Returns: CardTemplate[]

GET /templates/default
  - List only default Pokémon/MTG/modern templates
  - Returns: CardTemplate[]

POST /templates
  - Create custom template
  - Body: { name, description, template_json, preview_image_url? }
  - Returns: CardTemplate

PUT /templates/{templateId}
  - Update custom template
  - Returns: CardTemplate

DELETE /templates/{templateId}
  - Delete custom template (only user's own)
  - Returns: { success: true }

POST /templates/{templateId}/preview
  - Render template with sample data
  - Body: { sample_data }
  - Returns: { html_preview or react_component_data }
```

### File Upload
```
POST /upload/background
  - Upload card background image
  - Body: FormData (multipart/form-data)
  - Returns: { url: "https://..." }

POST /upload/template-preview
  - Upload preview image for custom template
  - Body: FormData
  - Returns: { url: "https://..." }
```

### GitHub Integration
```
GET /github/export-status/{deckId}
  - Check if deck is exported to GitHub
  - Returns: { is_exported, repo_url?, last_synced_at? }

POST /github/export
  - Export deck to GitHub
  - Body: { deck_id, repo_name?, visibility? }
  - Process:
    1. Serialize deck + cards to JSON
    2. Create/update GitHub repo
    3. Commit deck structure
    4. Log export in database
  - Returns: { success, repo_url }

POST /github/sync
  - Sync changes back to GitHub repo
  - Body: { deck_id }
  - Returns: { success, last_synced_at }

POST /github/import
  - Import deck from GitHub repository
  - Body: { github_repo_url }
  - Process:
    1. Fetch repo structure
    2. Parse deck JSON
    3. Create deck + cards locally
    4. Sync to Supabase
  - Returns: Deck
```

### Tags
```
GET /tags
  - List all user's tags
  - Returns: Tag[]

POST /tags
  - Create new tag
  - Body: { name, color? }
  - Returns: Tag

DELETE /tags/{tagId}
  - Delete tag (remove from all cards)
  - Returns: { success: true }
```

---

## 7. Storage Strategy

### Web Version (Supabase)
- **Database:** PostgreSQL (managed by Supabase)
- **File Storage:** Supabase Storage (AWS S3-backed)
  - Bucket: `card-backgrounds/` (user-uploaded images)
  - Bucket: `template-previews/` (custom template previews)
  - Bucket: `deck-exports/` (JSON exports for GitHub)
- **Vector DB:** pgvector extension in Postgres
- **Authentication:** Supabase Auth (GitHub OAuth)
- **Real-time (optional):** Supabase Realtime for live collaboration

### Desktop Version (Tauri)
- **Local Database:** SQLite
  - Location: `~/.promptdec/promptdec.db`
  - Same schema as web (portable)
- **File Storage:** Local file system
  - Location: `~/.promptdec/files/`
  - Structure: `backgrounds/`, `templates/`, `exports/`
- **Export Format:** JSON (compatible with GitHub/web)
- **No Authentication:** Local development mode

### GitHub as Interchange Format
- **Export Structure:**
  ```
  deck-name/
  ├── deck.json (metadata)
  ├── cards/
  │   ├── card-1.json
  │   ├── card-2.json
  │   └── ...
  └── assets/ (optional - embedded images as base64 or links)
  ```
- **deck.json schema:**
  ```json
  {
    "name": "Image Prompts",
    "description": "...",
    "created_at": "...",
    "cards": [
      {
        "id": "...",
        "front": { "template": "pokemon", "customizations": {...} },
        "back": { "content": "...", "format": "markdown" },
        "tags": ["image-gen", "advanced"],
        "favorite": false
      }
    ]
  }
  ```

---

## 8. Authentication & Authorization

### Web Version
- **Provider:** GitHub OAuth via Supabase Auth
- **Flow:**
  1. User clicks "Login with GitHub"
  2. Redirected to GitHub OAuth consent screen
  3. GitHub redirects back with `code`
  4. Frontend exchanges code for Supabase session token
  5. Token stored in localStorage
  6. All API requests include `Authorization: Bearer {token}`
- **Permissions Requested:**
  - `user:email` (public profile)
  - `repo` (read/write for deck exports)
- **Session Management:**
  - Supabase handles token refresh
  - Token valid for 1 hour, auto-refreshes
  - Logout clears localStorage + Supabase session

### Desktop Version
- **No Authentication Required**
- **Local-only Mode:**
  - Can use app completely offline
  - Manual GitHub push when ready (uses local GitHub credentials or token)
  - Optional: GitHub token stored locally for pushing

### Authorization
- **User can only access their own data:**
  ```
  WHERE user_id = current_user_id
  ```
- **Supabase RLS (Row Level Security) policies:**
  ```sql
  -- Users can only see/edit their own decks
  CREATE POLICY "Users can manage own decks"
    ON decks
    FOR ALL
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);
  ```

---

## 9. Semantic Search Implementation

### Overview
Semantic search allows users to find prompts by meaning/context, not exact keywords. Example: searching "data analysis tips" finds a card about statistical methods even if it doesn't contain those exact words.

### Architecture
```
User Query
  ↓
[Embed via OpenAI API]
  ↓
1536-dim vector
  ↓
[pgvector cosine similarity in Postgres]
  ↓
Top K results sorted by similarity score
```

### Implementation Details

**1. Embedding Generation (on card creation/edit)**
- When card is created or back_content is edited:
  - Extract card back_content (markdown)
  - Send to OpenAI Embeddings API (text-embedding-3-small)
  - Receive 1536-dimensional vector
  - Store in `cards.content_embedding`

**2. Search Query Processing**
```python
# FastAPI endpoint
@app.post("/search/semantic")
async def semantic_search(
    query: str,
    deck_id: Optional[UUID] = None,
    limit: int = 10,
    threshold: float = 0.7
):
    # 1. Embed query
    query_embedding = openai.Embedding.create(
        model="text-embedding-3-small",
        input=query
    )['data'][0]['embedding']
    
    # 2. Vector search in Postgres
    scope = "ALL DECKS" if not deck_id else f"deck_id={deck_id}"
    results = await db.execute(f"""
      SELECT id, back_content, 1 - (
        content_embedding <-> $1
      ) as similarity
      FROM cards
      WHERE user_id = $2
        {f"AND deck_id = '{deck_id}'" if deck_id else ""}
        AND 1 - (content_embedding <-> $1) > $3
      ORDER BY content_embedding <-> $1
      LIMIT $4
    """, query_embedding, user_id, threshold, limit)
    
    return results
```

**3. Search Scope (Dynamic)**
- **From Homepage (Decks view):** Search all user's decks
- **From Deck View:** Search only current deck
- Query includes scope in API call

**4. Performance Considerations**
- **Index:** `CREATE INDEX ON cards USING IVFFLAT (content_embedding)`
- **Batch Embeddings:** Generate embeddings on background queue for imported decks
- **Caching:** Cache recent searches (Redis optional)
- **Rate Limiting:** OpenAI embeddings API costs

---

## 10. Card Template System

### Template Architecture

**Templates are JSON schemas that define:**
1. **Layout zones** (title area, artwork, metadata)
2. **Styling rules** (colors, fonts, borders)
3. **Responsive behavior**

**Flow: JSON → React Component (Runtime)**

### Default Templates (Pre-seeded)

#### 1. Pokémon Template
```json
{
  "id": "template-pokemon",
  "name": "Pokémon",
  "description": "Classic Pokémon card style",
  "zones": [
    { "id": "background", "type": "image", "position": "full" },
    { "id": "title", "type": "text", "position": "top", "size": "large" },
    { "id": "metadata", "type": "text", "position": "bottom", "size": "small" }
  ],
  "styles": {
    "borderColor": "#FFD700",
    "borderWidth": "4px",
    "backgroundColor": "rgba(0,0,0,0.7)",
    "titleColor": "#FFFFFF",
    "borderRadius": "12px"
  }
}
```

#### 2. Modern Art Template
```json
{
  "id": "template-modern",
  "name": "Modern Art",
  "description": "Minimalist with centered artwork",
  "zones": [
    { "id": "background", "type": "image", "position": "center" },
    { "id": "title", "type": "text", "position": "top-center", "size": "small" }
  ],
  "styles": {
    "backgroundColor": "#000000",
    "borderColor": "#FFFFFF",
    "borderWidth": "2px"
  }
}
```

#### 3. MTG-style Template
(Gold borders, elaborate layout)

#### 4. Minimalist Template
(Clean, no artwork, text-focused)

### Custom Template Creation

**User can:**
1. **Use template builder UI** (visual editor)
2. **Import React component** (for advanced users)

**Custom template JSON example:**
```json
{
  "id": "custom-template-123",
  "name": "My Custom Design",
  "is_custom": true,
  "zones": [
    { "id": "background", "type": "image" },
    { "id": "gradient", "type": "gradient", "colors": ["#FF0000", "#0000FF"] },
    { "id": "title", "type": "text", "position": "top-left" },
    { "id": "custom_zone", "type": "html", "html": "<div>Custom HTML</div>" }
  ],
  "styles": { ... },
  "responsive": {
    "mobile": { ... },
    "tablet": { ... }
  }
}
```

### Template Rendering (Frontend)

```typescript
// CardFront.tsx
import { renderTemplate } from "@/utils/cardRenderer";

interface CardFrontProps {
  template: CardTemplate;
  customization: FrontCustomization;
  backgroundUrl?: string;
  title?: string;
  colors?: ColorPalette;
}

export function CardFront(props: CardFrontProps) {
  // If template has custom React component
  if (props.template.custom_react_component) {
    return <DynamicComponent {...props} />;
  }
  
  // Otherwise, render from JSON schema
  const renderedComponent = renderTemplate(
    props.template.template_json,
    props.customization
  );
  
  return renderedComponent;
}
```

**cardRenderer.ts:**
```typescript
export function renderTemplate(
  schema: TemplateJson,
  customization: FrontCustomization
): React.ReactNode {
  // Dynamically build React component from template schema
  // Apply customizations (background URL, colors, title)
  // Return responsive JSX
}
```

### React Component Import

**Advanced users can import custom React components:**

```typescript
// User provides React component
function MyCustomCard(props) {
  return (
    <div className="card" style={{ background: props.backgroundUrl }}>
      <h1>{props.title}</h1>
      <img src={props.backgroundUrl} />
    </div>
  );
}

// Component is stored in database as stringified code
// On render, it's executed with props
```

---

## 11. GitHub Integration & Sync Logic

### Export Flow (Web → GitHub)

```
User clicks "Export to GitHub"
  ↓
ExportModal: User chooses repo name, visibility
  ↓
POST /github/export { deck_id, repo_name }
  ↓
[Backend]
  1. Fetch deck + all cards
  2. Serialize to JSON structure
  3. Create GitHub repo via GitHub API
  4. Commit deck.json + cards/
  5. Store repo URL in github_exports table
  6. Return repo URL
  ↓
ExportModal: "Successfully exported! View on GitHub"
```

**Export JSON Structure:**
```
my-prompts/
├── README.md (generated)
├── deck.json
└── cards/
    ├── card-1.json
    ├── card-2.json
    └── ...
```

### Import Flow (GitHub → Web)

```
User provides GitHub repo URL
  ↓
POST /github/import { repo_url }
  ↓
[Backend]
  1. Fetch repo contents via GitHub API
  2. Parse deck.json + cards/*.json
  3. Create deck in Supabase
  4. Create all cards
  5. Generate embeddings
  6. Log in github_exports
  ↓
Frontend: Deck appears in deck list, auto-synced
```

### Sync (Desktop → GitHub)

```
Desktop (Tauri) user has local deck
  ↓
User clicks "Push to GitHub"
  ↓
[Tauri/Backend]
  1. Serialize local deck to JSON
  2. Create GitHub repo (or update existing)
  3. Commit changes
  4. Return repo URL
  ↓
User can share repo link
```

### Sync (GitHub → Desktop)

```
Desktop user provides GitHub repo URL
  ↓
Tauri app fetches repo JSON
  ↓
Deserialize to local SQLite
  ↓
Deck appears in local deck list
```

### Conflict Resolution
- **One-directional by design** (GitHub is source of truth from one platform)
- If desktop user pushes to GitHub, then logs into web version:
  - Web version auto-syncs by fetching from GitHub
  - Changes from web override (one-directional push)
  - No merge logic needed (reduces complexity)

---

## 12. File Upload & Storage Pipeline

### Background Image Upload

```
User clicks "Upload Background" in CardBuilder
  ↓
FileUploadZone shows drag-and-drop area
  ↓
User selects/drags file
  ↓
[Frontend Validation]
  1. Check file type (jpg, png, webp)
  2. Check file size < 5MB
  3. Show preview
  ↓
User confirms upload
  ↓
POST /upload/background FormData
  ↓
[Backend]
  1. Validate file again
  2. Optimize/compress image
  3. Upload to Supabase Storage (card-backgrounds/)
  4. Return signed URL
  ↓
Frontend: URL stored in card.front_background_url
```

### Custom Template Preview Upload

```
Similar flow
  ↓
POST /upload/template-preview
  ↓
Supabase Storage (template-previews/)
  ↓
URL returned to template editor
```

### Desktop Version (Tauri)

```
User selects local file
  ↓
Tauri file system API reads file
  ↓
File stored in ~/.promptdec/files/backgrounds/
  ↓
Local path stored in SQLite
  ↓
On export to GitHub: base64 encode file or link to it
```

---

## 13. Keyboard Shortcuts & UI Interactions

### Global Shortcuts
```
Cmd/Ctrl + N  →  Create new deck (homepage)
             OR Create new card (inside deck)

Cmd/Ctrl + /  →  Focus semantic search bar

Cmd/Ctrl + S  →  Save card (in edit mode)

Esc           →  Close modals, exit edit mode
```

### Contextual UI
```
Homepage
  └─ Cmd+N → CreateDeckModal

Deck View
  └─ Cmd+N → CreateCardModal
  └─ FAB button → CreateCardModal

Card View (edit mode)
  └─ Cmd+S → Save & Sync
  └─ Esc → Cancel edit
```

### Hover & Animation
```
Deck Card (homepage)
  └─ Hover → Lift effect, shadow

Card Thumbnail (deck view)
  └─ Hover → Brighten, scale 1.05

Card (flipped view)
  └─ 3D Flip animation (0.6s)
  └─ Front face on click
  └─ Back face on click
  └─ Smooth interpolation with Framer Motion
```

---

## 14. Semantic Search Bar Animation & Interaction

### Default State
- Small icon + text in center-top of navbar
- Shows hint: "Cmd+/ to search"

### On Click / Cmd+/
- Bar expands to full width (smooth animation)
- Input field gains focus
- Placeholder: "Search by context... (e.g., 'data analysis')"

### While Typing
- Real-time results appear below (dropdown)
- Shows cards from current scope (all decks or specific deck)
- Relevance score displayed

### Scope Indicator
- If on homepage: "Searching all decks"
- If in deck: "Searching [Deck Name]"

---

## 15. Keyboard Shortcut Implementation

```typescript
// useKeyboardShortcuts.ts
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCreateDeckModal, useCreateCardModal } from '@/stores/uiStore';

export function useKeyboardShortcuts() {
  const navigate = useNavigate();
  const { openCreateDeck } = useCreateDeckModal();
  const { openCreateCard } = useCreateCardModal();
  const { currentDeckId } = useCurrentDeck(); // from Zustand
  
  useEffect(() => {
    function handleKeyDown(e: KeyboardEvent) {
      if (e.metaKey || e.ctrlKey) {
        if (e.key === 'n') {
          e.preventDefault();
          // If on homepage, create deck; if in deck, create card
          if (!currentDeckId) {
            openCreateDeck();
          } else {
            openCreateCard(currentDeckId);
          }
        }
        if (e.key === '/') {
          e.preventDefault();
          // Focus search bar
          document.getElementById('semantic-search-input')?.focus();
        }
        if (e.key === 's') {
          e.preventDefault();
          // Save in edit mode (if applicable)
          window.dispatchEvent(new CustomEvent('save-card'));
        }
      }
      if (e.key === 'Escape') {
        // Close modals
        window.dispatchEvent(new CustomEvent('close-modals'));
      }
    }
    
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [currentDeckId]);
}
```

---

## 16. 3D Card Flip Animation

```typescript
// CardFlip.tsx
import { motion } from 'framer-motion';
import { useState } from 'react';

interface CardFlipProps {
  front: React.ReactNode;
  back: React.ReactNode;
}

export function CardFlip({ front, back }: CardFlipProps) {
  const [isFlipped, setIsFlipped] = useState(false);
  
  return (
    <motion.div
      onClick={() => setIsFlipped(!isFlipped)}
      className="card-flip-container"
      style={{
        perspective: '1000px',
        cursor: 'pointer',
        width: '300px',
        height: '400px'
      }}
      whileHover={{ scale: 1.02 }}
    >
      <motion.div
        initial={false}
        animate={{ rotateY: isFlipped ? 180 : 0 }}
        transition={{ duration: 0.6, type: 'spring', stiffness: 60 }}
        style={{
          transformStyle: 'preserve-3d',
          width: '100%',
          height: '100%'
        }}
      >
        {/* Front */}
        <motion.div
          style={{
            backfaceVisibility: 'hidden',
            WebkitBackfaceVisibility: 'hidden'
          }}
          className="card-front"
        >
          {front}
        </motion.div>
        
        {/* Back */}
        <motion.div
          initial={{ rotateY: 180 }}
          animate={{ rotateY: isFlipped ? 0 : 180 }}
          transition={{ duration: 0.6, type: 'spring', stiffness: 60 }}
          style={{
            backfaceVisibility: 'hidden',
            WebkitBackfaceVisibility: 'hidden',
            position: 'absolute',
            width: '100%',
            height: '100%',
            top: 0,
            left: 0
          }}
          className="card-back"
        >
          {back}
        </motion.div>
      </motion.div>
    </motion.div>
  );
}
```

---

## 17. Drag-and-Drop File Upload

```typescript
// FileUploadZone.tsx
import { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';

export function FileUploadZone({ onFileSelect }: Props) {
  const [isDragActive, setIsDragActive] = useState(false);
  
  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      onFileSelect(acceptedFiles[0]);
      setIsDragActive(false);
    }
  }, [onFileSelect]);
  
  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    accept: { 'image/*': ['.jpeg', '.jpg', '.png', '.webp'] },
    maxSize: 5 * 1024 * 1024 // 5MB
  });
  
  return (
    <motion.div
      {...getRootProps()}
      animate={{
        scale: isDragActive ? 1.05 : 1,
        borderColor: isDragActive ? '#3B82F6' : '#D1D5DB'
      }}
      className={`
        border-2 border-dashed rounded-lg p-8 text-center
        ${isDragActive ? 'bg-blue-50' : 'bg-gray-50'}
      `}
      onDragEnter={() => setIsDragActive(true)}
      onDragLeave={() => setIsDragActive(false)}
    >
      <input {...getInputProps()} />
      <p className="text-gray-600">
        {isDragActive 
          ? 'Drop file here' 
          : 'Drag & drop or click to select'}
      </p>
    </motion.div>
  );
}
```

---

## 18. React Query Setup (TanStack Query)

```typescript
// hooks/useDecks.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/api/client';

export function useDecks() {
  return useQuery({
    queryKey: ['decks'],
    queryFn: async () => api.get('/decks'),
    staleTime: 5 * 60 * 1000 // 5 minutes
  });
}

export function useCreateDeck() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (data: CreateDeckPayload) => 
      api.post('/decks', data),
    onSuccess: () => {
      // Invalidate decks list to refetch
      queryClient.invalidateQueries({ queryKey: ['decks'] });
    }
  });
}

export function useCards(deckId: string) {
  return useQuery({
    queryKey: ['cards', deckId],
    queryFn: async () => api.get(`/decks/${deckId}/cards`),
    enabled: !!deckId
  });
}

export function useUpdateCard() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ cardId, data }: UpdateCardPayload) =>
      api.put(`/cards/${cardId}`, data),
    onSuccess: (data) => {
      // Update cache immediately
      queryClient.setQueryData(['card', data.id], data);
    }
  });
}
```

---

## 19. Zustand Store Setup

```typescript
// stores/uiStore.ts
import { create } from 'zustand';

interface UIStore {
  // Modals
  isCreateDeckModalOpen: boolean;
  isCreateCardModalOpen: boolean;
  isCardBuilderOpen: boolean;
  
  // Current context
  currentDeckId: string | null;
  currentCardId: string | null;
  
  // View mode
  cardViewMode: 'grid' | 'list';
  
  // Actions
  openCreateDeckModal: () => void;
  closeCreateDeckModal: () => void;
  openCreateCardModal: (deckId: string) => void;
  closeCreateCardModal: () => void;
  setCardViewMode: (mode: 'grid' | 'list') => void;
}

export const useUIStore = create<UIStore>((set) => ({
  isCreateDeckModalOpen: false,
  isCreateCardModalOpen: false,
  isCardBuilderOpen: false,
  currentDeckId: null,
  currentCardId: null,
  cardViewMode: 'grid',
  
  openCreateDeckModal: () => set({ isCreateDeckModalOpen: true }),
  closeCreateDeckModal: () => set({ isCreateDeckModalOpen: false }),
  // ... rest of actions
}));
```

---

## 20. Implementation Challenges & Solutions

### Challenge 1: Vector Embedding Costs
**Problem:** OpenAI embeddings API has usage costs. Generating embeddings for every card could be expensive.

**Solutions:**
- Batch embed on import (not individual cards)
- Cache embeddings per deck
- Consider local embedding models for desktop (Ollama + embeddings)
- Rate limit search requests

### Challenge 2: Real-time Sync (Web)
**Problem:** Multiple users might edit same deck simultaneously.

**Solutions:**
- Implement Supabase Realtime for collaborative features (future)
- For MVP: Simple "last write wins" conflict resolution
- Add "refresh" button to pull latest changes

### Challenge 3: Template Rendering Complexity
**Problem:** Custom React components could be malicious or break rendering.

**Solutions:**
- Sandbox custom React components (React.lazy + error boundary)
- Validate template JSON schema before execution
- Provide template builder UI (no direct code input for non-devs)

### Challenge 4: GitHub API Rate Limiting
**Problem:** Exporting decks makes GitHub API requests; could hit rate limits.

**Solutions:**
- Implement request queuing/debouncing
- Cache GitHub responses
- Use GitHub tokens for higher limits
- Batch exports (don't export on every card create)

### Challenge 5: Desktop SQLite Sync
**Problem:** How to sync local SQLite with cloud when moving between desktop and web?

**Solutions:**
- Manual export-to-GitHub (clear, explicit)
- Local backup mechanism (export to JSON before switching)
- Clear UX messaging about sync points

### Challenge 6: Embedding Generation on Import
**Problem:** Importing large deck from GitHub means generating many embeddings sequentially.

**Solutions:**
- Background job queue (Celery + Redis)
- Batch embedding API calls (OpenAI supports bulk)
- Show progress indicator to user
- Cache recently generated embeddings

---

## 21. Deployment Strategy

### Web (Phase 1)

**Frontend (Vercel)**
```
repo/
├── apps/web/
│   └── [Vite + React app]
└── apps/backend/
    └── [FastAPI app]

1. Push to GitHub
2. Vercel auto-deploys from main branch
3. Environment variables:
   - VITE_API_URL=https://api.promptdec.com
   - VITE_SUPABASE_URL
   - VITE_SUPABASE_ANON_KEY
   - VITE_GITHUB_CLIENT_ID
```

**Backend (Railway/Render)**
```
1. Deploy FastAPI app
2. Connect to Supabase PostgreSQL
3. Environment variables:
   - DATABASE_URL
   - OPENAI_API_KEY
   - GITHUB_TOKEN
   - GITHUB_CLIENT_SECRET
4. Auto-deploy on main branch push
```

**Database (Supabase)**
```
1. Create Supabase project
2. Run migrations (SQL scripts)
3. Set up auth (GitHub OAuth)
4. Configure storage buckets (card-backgrounds, etc.)
5. Enable pgvector extension
6. Set up RLS policies
```

### Desktop (Phase 2)

**Tauri Build**
```
1. npm run tauri build
2. Creates installers for Windows, macOS, Linux
3. Sign binaries with certificates
4. Distribute via GitHub Releases
```

### Environment Configuration

**Web .env.local**
```
VITE_API_URL=http://localhost:3001 (dev) or https://api.promptdec.com (prod)
VITE_SUPABASE_URL=...
VITE_SUPABASE_ANON_KEY=...
VITE_GITHUB_CLIENT_ID=...
```

**Backend .env**
```
DATABASE_URL=postgresql://user:pass@...
OPENAI_API_KEY=...
GITHUB_TOKEN=...
GITHUB_CLIENT_SECRET=...
SUPABASE_SERVICE_KEY=...
CORS_ORIGINS=http://localhost:5173,https://promptdec.com
```

---

## 22. Testing Strategy

### Unit Tests (Frontend)
- Component rendering (React Testing Library)
- Custom hooks (useDecks, useSemanticSearch)
- Utility functions (markdown parsing, template rendering)

### Integration Tests (Frontend)
- Card builder flow (select template → customize → preview → create)
- Semantic search (query → results display)
- GitHub export (deck serialization → API call)

### Backend Tests (FastAPI)
- API endpoints (CRUD operations)
- Semantic search logic
- Template rendering
- GitHub API integration
- Authentication/authorization

### E2E Tests (Playwright/Cypress)
- User flow: Create deck → Add card → Customize → Search → Export
- Cross-platform: Web to GitHub to Desktop sync

---

## 23. Future Enhancements (Post-MVP)

1. **Collaborative Decks** (multiple users editing same deck)
2. **Card Ratings** (community ratings on shared decks)
3. **Card Versioning** (track changes to cards over time)
4. **Mobile App** (React Native or Flutter)
5. **Advanced Analytics** (usage stats, popular cards)
6. **Custom Embedding Models** (local embeddings for privacy)
7. **Deck Templates** (preset deck structures)
8. **AI-assisted Card Generation** (suggest improvements)
9. **Browser Extension** (quick access from anywhere)
10. **API for Third-party Apps** (PromptDec as backend)

---

## 24. Architecture Decision Records (ADRs)

### ADR-001: Why pgvector for Semantic Search?
**Decision:** Use pgvector extension in PostgreSQL for vector similarity search.

**Rationale:**
- Already using Supabase (PostgreSQL)
- Avoids additional infrastructure (separate vector DB)
- Good performance for MVP scale
- Can scale to dedicated vector DB later

**Alternative Considered:** Pinecone, Weaviate (overkill for MVP)

---

### ADR-002: Why JSON Schema for Templates?
**Decision:** Define card templates as JSON schemas that render to React components.

**Rationale:**
- Allows power users to customize via UI
- Advanced users can import React components
- No need for separate template engine
- Runtime flexibility

**Alternative Considered:** Static template definitions (less flexible)

---

### ADR-003: Why One-Directional GitHub Sync?
**Decision:** GitHub exports are one-directional (push only, no pull/merge).

**Rationale:**
- Reduces conflict resolution complexity
- Clear data ownership (GitHub is source for exported decks)
- Desktop and web remain independent
- Can add bidirectional sync later

**Alternative Considered:** Bidirectional sync with conflict resolution (more complex)

---

## 25. Security Considerations

### Frontend Security
- **XSS Prevention:** Sanitize markdown rendering (remark-gfm + xss library)
- **CSRF Protection:** Supabase Auth handles CSRF tokens
- **Secure Storage:** GitHub token stored in secure storage (Tauri)
- **Input Validation:** Validate all user inputs before sending to API

### Backend Security
- **Authentication:** All endpoints require valid Supabase token
- **Authorization:** RLS policies enforce user data isolation
- **Rate Limiting:** Rate limit API endpoints (OpenAI embeddings, GitHub)
- **Secrets:** Use environment variables, never hardcode
- **HTTPS Only:** All API calls over HTTPS
- **SQL Injection:** Use parameterized queries (SQLAlchemy ORM)

### Data Privacy
- **User Data:** Only owner can access their decks/cards
- **File Storage:** Supabase Storage has built-in access controls
- **Embeddings:** Stored securely, only used for search
- **GitHub:** User controls what's exported (explicit action)

---

## 26. Monitoring & Observability

### Frontend
- **Error Tracking:** Sentry for JavaScript errors
- **Analytics:** Segment for user behavior (optional)
- **Performance:** Web Vitals monitoring

### Backend
- **Logging:** Structured logging (Python logging)
- **Error Tracking:** Sentry for backend errors
- **Performance Monitoring:** APM tool (New Relic or Datadog)
- **Database Monitoring:** Supabase built-in monitoring

### Alerts
- API endpoint errors
- High OpenAI API usage
- Database connection issues
- GitHub API rate limit warnings

---

## 27. Summary & Next Steps

### MVP Scope (Phase 1: Web)
✅ Deck & card CRUD operations
✅ Card customization (premade templates)
✅ Semantic search (context-aware)
✅ GitHub OAuth authentication
✅ Export deck to GitHub
✅ 3D card flip animation
✅ Click-to-flip with hover effects
✅ Markdown support (render + edit)
✅ Tags and favorites
✅ Responsive design

### Immediate Todos
1. **Database Schema** → Run SQL migrations in Supabase
2. **Backend Setup** → FastAPI skeleton + endpoints
3. **Frontend Setup** → Vite + React scaffold
4. **Components** → Build component library (CardFlip, FileUploadZone, etc.)
5. **Authentication** → Integrate Supabase Auth + GitHub OAuth
6. **Semantic Search** → Integrate OpenAI Embeddings API
7. **Testing** → Set up test suite
8. **Deployment** → Configure Vercel + Railway
9. **Documentation** → API docs, user guide

### Phase 2 (Desktop)
- Tauri setup
- SQLite integration
- GitHub export (desktop)
- Cross-platform sync strategy

---

## Conclusion

PromptDec is architected as a scalable, user-friendly prompt management tool with semantic search capabilities and cross-platform support. The MVP focuses on the web version with a robust backend, while the desktop version leverages the same architecture with local storage. GitHub integration enables community sharing and future collaboration features.

This document provides a comprehensive blueprint for implementation with agentic coding models and is ready for architectural review by higher-tier Claude models.

