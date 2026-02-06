-- Seed Default Card Templates
-- Phase 1A: Database Setup

-- Template 1: Pokémon Style
INSERT INTO card_templates (id, user_id, name, description, is_default, template_json, created_at)
VALUES (
  'template-pokemon',
  NULL,
  'Pokémon Classic',
  'Classic Pokémon card style with gold border',
  TRUE,
  '{
    "zones": [
      {"id": "background", "type": "image", "position": "full"},
      {"id": "title", "type": "text", "position": "top", "size": "large"},
      {"id": "metadata", "type": "text", "position": "bottom", "size": "small"}
    ],
    "styles": {
      "borderColor": "#FFD700",
      "borderWidth": "4px",
      "backgroundColor": "rgba(0,0,0,0.7)",
      "titleColor": "#FFFFFF",
      "borderRadius": "12px"
    }
  }',
  datetime('now')
);

-- Template 2: Modern Art
INSERT INTO card_templates (id, user_id, name, description, is_default, template_json, created_at)
VALUES (
  'template-modern',
  NULL,
  'Modern Art',
  'Minimalist with centered artwork',
  TRUE,
  '{
    "zones": [
      {"id": "background", "type": "image", "position": "center"},
      {"id": "title", "type": "text", "position": "top-center", "size": "small"}
    ],
    "styles": {
      "backgroundColor": "#000000",
      "borderColor": "#FFFFFF",
      "borderWidth": "2px",
      "titleColor": "#FFFFFF",
      "borderRadius": "8px"
    }
  }',
  datetime('now')
);

-- Template 3: MTG Style
INSERT INTO card_templates (id, user_id, name, description, is_default, template_json, created_at)
VALUES (
  'template-mtg',
  NULL,
  'Magic: The Gathering',
  'MTG-inspired with ornate borders',
  TRUE,
  '{
    "zones": [
      {"id": "background", "type": "image", "position": "center"},
      {"id": "title", "type": "text", "position": "top", "size": "medium"},
      {"id": "border", "type": "gradient", "colors": ["#C9A961", "#8B7355"]}
    ],
    "styles": {
      "borderColor": "#C9A961",
      "borderWidth": "3px",
      "backgroundColor": "rgba(0,0,0,0.8)",
      "titleColor": "#FFFFFF",
      "borderRadius": "10px"
    }
  }',
  datetime('now')
);

-- Template 4: Minimalist
INSERT INTO card_templates (id, user_id, name, description, is_default, template_json, created_at)
VALUES (
  'template-minimal',
  NULL,
  'Minimalist',
  'Clean, text-focused design',
  TRUE,
  '{
    "zones": [
      {"id": "title", "type": "text", "position": "top", "size": "medium"}
    ],
    "styles": {
      "backgroundColor": "#FFFFFF",
      "borderColor": "#E0E0E0",
      "borderWidth": "1px",
      "titleColor": "#000000",
      "borderRadius": "4px"
    }
  }',
  datetime('now')
);
