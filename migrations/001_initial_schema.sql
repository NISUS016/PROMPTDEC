-- PromptDec Database Schema - Phase 1A
-- Universal schema compatible with SQLite and PostgreSQL
-- Target: Supabase (PostgreSQL)

-- Enable UUID extension (PostgreSQL only)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table (managed by Supabase Auth)
CREATE TABLE IF NOT EXISTS users (
  id TEXT PRIMARY KEY,
  github_id INTEGER UNIQUE,
  github_username VARCHAR(255),
  display_name VARCHAR(255),
  avatar_url TEXT,
  created_at TEXT DEFAULT (datetime('now')),
  updated_at TEXT DEFAULT (datetime('now'))
);

-- Decks table
CREATE TABLE IF NOT EXISTS decks (
  id TEXT PRIMARY KEY DEFAULT (uuid_generate_v4()::text),
  user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  artwork_url TEXT,
  is_public BOOLEAN DEFAULT FALSE,
  created_at TEXT DEFAULT (datetime('now')),
  updated_at TEXT DEFAULT (datetime('now')),
  UNIQUE(user_id, name)
);

-- Card templates table
CREATE TABLE IF NOT EXISTS card_templates (
  id TEXT PRIMARY KEY DEFAULT (uuid_generate_v4()::text),
  user_id TEXT REFERENCES users(id) ON DELETE CASCADE,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  is_default BOOLEAN DEFAULT FALSE,
  template_json TEXT, -- JSON schema as string
  preview_image_url TEXT,
  created_at TEXT DEFAULT (datetime('now')),
  updated_at TEXT DEFAULT (datetime('now')),
  UNIQUE(user_id, name)
);

-- Cards table (universal schema)
CREATE TABLE IF NOT EXISTS cards (
  id TEXT PRIMARY KEY DEFAULT (uuid_generate_v4()::text),
  deck_id TEXT NOT NULL REFERENCES decks(id) ON DELETE CASCADE,
  user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  
  -- Front (visual)
  front_template_id TEXT REFERENCES card_templates(id),
  front_custom_json TEXT, -- JSON object as string
  front_background_url TEXT,
  front_title VARCHAR(255),
  front_custom_colors TEXT, -- JSON: {"primary": "#FF0000", ...}
  
  -- Back (content)
  back_content TEXT, -- markdown
  back_format TEXT DEFAULT 'markdown', -- 'markdown' | 'txt'
  
  -- Metadata
  tags TEXT, -- JSON array: ["tag1", "tag2"]
  is_favorite BOOLEAN DEFAULT FALSE,
  
  -- Embeddings (universal format)
  content_embedding TEXT, -- JSON array: [0.123, 0.456, ...]
  
  created_at TEXT DEFAULT (datetime('now')),
  updated_at TEXT DEFAULT (datetime('now'))
);

-- GitHub exports tracking
CREATE TABLE IF NOT EXISTS github_exports (
  id TEXT PRIMARY KEY DEFAULT (uuid_generate_v4()::text),
  user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  deck_id TEXT NOT NULL REFERENCES decks(id) ON DELETE CASCADE,
  github_repo_url TEXT,
  last_exported_at TEXT,
  last_synced_at TEXT,
  created_at TEXT DEFAULT (datetime('now'))
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_cards_deck_id ON cards(deck_id);
CREATE INDEX IF NOT EXISTS idx_cards_user_id ON cards(user_id);
CREATE INDEX IF NOT EXISTS idx_cards_favorite ON cards(is_favorite);
CREATE INDEX IF NOT EXISTS idx_decks_user_id ON decks(user_id);
CREATE INDEX IF NOT EXISTS idx_github_exports_user_id ON github_exports(user_id);

-- PostgreSQL-specific optimization: Add pgvector column
-- Execute this AFTER base schema
-- ALTER TABLE cards ADD COLUMN IF NOT EXISTS content_embedding_pgvector vector(384);

-- Create pgvector index (PostgreSQL only)
-- CREATE INDEX IF NOT EXISTS idx_cards_embedding ON cards 
-- USING ivfflat (content_embedding_pgvector vector_cosine_ops);

-- Trigger to sync TEXT → pgvector (PostgreSQL only)
-- CREATE OR REPLACE FUNCTION sync_embeddings() RETURNS TRIGGER AS $$
-- BEGIN
--   IF NEW.content_embedding IS NOT NULL THEN
--     NEW.content_embedding_pgvector := (NEW.content_embedding::jsonb)::vector;
--   END IF;
--   RETURN NEW;
-- END;
-- $$ LANGUAGE plpgsql;

-- CREATE TRIGGER trigger_sync_embeddings
--   BEFORE INSERT OR UPDATE ON cards
--   FOR EACH ROW
--   EXECUTE FUNCTION sync_embeddings();

-- Row-Level Security (RLS) policies
-- Enable RLS
ALTER TABLE decks ENABLE ROW LEVEL SECURITY;
ALTER TABLE cards ENABLE ROW LEVEL SECURITY;
ALTER TABLE card_templates ENABLE ROW LEVEL SECURITY;
ALTER TABLE github_exports ENABLE ROW LEVEL SECURITY;

-- RLS Policies
CREATE POLICY "Users can manage own decks" ON decks
  FOR ALL USING (auth.uid()::text = user_id);

CREATE POLICY "Users can manage own cards" ON cards
  FOR ALL USING (auth.uid()::text = user_id);

CREATE POLICY "Users can manage own templates" ON card_templates
  FOR ALL USING (auth.uid()::text = user_id OR is_default = TRUE);

CREATE POLICY "Users can view default templates" ON card_templates
  FOR SELECT USING (is_default = TRUE);

CREATE POLICY "Users can manage own exports" ON github_exports
  FOR ALL USING (auth.uid()::text = user_id);
