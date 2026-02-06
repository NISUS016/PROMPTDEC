# PromptDec - Quick Implementation Checklist

**Purpose:** High-level task checklist for rapid progress tracking  
**Last Updated:** 2026-02-06

---

## 🎯 Phase 0: Setup (Week 1)

- [ ] Initialize Git repository
- [ ] Set up Node.js + Python environment
- [ ] Create Supabase project
- [ ] Configure `.env` files
- [ ] Set up Sentry (optional)

**Goal:** Development environment ready

---

## 💾 Phase 1A: Database (Week 1)

- [ ] Write SQL schema migration
- [ ] Create all tables (users, decks, cards, templates, github_exports)
- [ ] Add PostgreSQL optimizations (pgvector column + trigger)
- [ ] Seed 4 default templates
- [ ] Enable Row-Level Security (RLS)
- [ ] Create Supabase Storage buckets

**Goal:** Database schema deployed to Supabase

---

## 🖥️ Phase 1B: Backend (Week 2)

- [ ] FastAPI skeleton + health endpoint
- [ ] Database connection (SQLAlchemy)
- [ ] Authentication middleware (JWT validation)
- [ ] CRUD endpoints - Decks (GET, POST, PUT, DELETE)
- [ ] CRUD endpoints - Cards (GET, POST, PUT, DELETE, duplicate)
- [ ] Error handling + Sentry integration

**Goal:** Backend API functional

---

## ⚛️ Phase 1C: Frontend (Week 2)

- [ ] Vite + React + TypeScript setup
- [ ] Install Tailwind CSS + Shadcn/UI
- [ ] React Router (routes: /, /decks/:id, /cards/:id)
- [ ] API client with auth headers
- [ ] Zustand stores (UI, auth)
- [ ] React Query provider

**Goal:** Frontend foundation ready

---

## 🔍 Phase 2A: Semantic Search (Week 3)

- [ ] Install `@xenova/transformers`
- [ ] Create `useEmbedding` hook (model loading)
- [ ] Implement embedding cache (localStorage)
- [ ] Auto-embed on card save
- [ ] Semantic search function (cosine similarity)
- [ ] Search UI component (animated bar)

**Goal:** Semantic search working end-to-end

---

## 🃏 Phase 2B: Card System (Week 3-4)

- [ ] Card template renderer (JSON → React)
- [ ] CardFront component
- [ ] CardBack component (markdown rendering)
- [ ] 3D flip animation (Framer Motion)
- [ ] CardGrid view (responsive)
- [ ] CardList view

**Goal:** Card display + animations complete

---

## 🎨 Phase 3A: Card Builder (Week 4-5)

- [ ] Template selector
- [ ] Front customizer (colors, title)
- [ ] File upload zone (drag-and-drop)
- [ ] Back content editor (markdown)
- [ ] Tag editor
- [ ] Live preview
- [ ] Card builder modal (full-screen)

**Goal:** Card creation workflow complete

---

## 🐙 Phase 3B: GitHub Integration (Week 5)

- [ ] Deck serialization utility (JSON export)
- [ ] Export modal (manual repo URL input)
- [ ] Backend export endpoint (POST /github/export)
- [ ] Import modal
- [ ] Backend import endpoint (POST /github/import)
- [ ] Sync status UI

**Goal:** GitHub export/import working

---

## 🎭 Phase 4A: UI Polish (Week 6)

- [ ] Main layout (header, sidebar, content)
- [ ] Navbar (logo, search, user menu)
- [ ] Sidebar (deck list, favorites, tags)
- [ ] HomePage (deck grid)
- [ ] DeckView (card grid/list)
- [ ] CardView (full-screen flip)

**Goal:** Complete UI layout

---

## ⌨️ Phase 4B: Interactions (Week 6)

- [ ] Keyboard shortcuts hook (Cmd+N, Cmd+/, Cmd+S, Esc)
- [ ] Hover effects (Framer Motion)
- [ ] Loading states + spinners
- [ ] Toast notifications
- [ ] Modal animations

**Goal:** Polished interactions

---

## 🔐 Phase 5A: Authentication (Week 7)

- [ ] Configure GitHub OAuth in Supabase
- [ ] Login page ("Login with GitHub")
- [ ] Auth callback handler
- [ ] Auth guard (protect routes)
- [ ] User profile display
- [ ] Logout functionality

**Goal:** Authentication working

---

## 🧪 Phase 5B: Testing (Week 7-8)

- [ ] Unit tests - Frontend (embeddings, search)
- [ ] Unit tests - Backend (CRUD, auth)
- [ ] Integration tests (card builder flow)
- [ ] E2E tests (Playwright: login → create → search → export)
- [ ] Performance tests (search speed, rendering)

**Goal:** 90%+ test coverage

---

## 🚀 Phase 6: Deployment (Week 8)

- [ ] Deploy backend to Railway/Render
- [ ] Deploy frontend to Vercel
- [ ] Run database migrations in production
- [ ] Configure custom domain (optional)
- [ ] Set up monitoring (Sentry, Vercel Analytics)
- [ ] Performance optimization (caching, code splitting)

**Goal:** Production deployment live

---

## 🖥️ Phase 7: Desktop (Optional, Week 9-10)

- [ ] Tauri setup + config
- [ ] SQLite integration
- [ ] File system API (local storage)
- [ ] Local search (Transformers.js)
- [ ] GitHub export (desktop)
- [ ] Build installers (Windows, macOS, Linux)

**Goal:** Desktop version released

---

## 📊 Success Metrics

**Technical:**
- [ ] All endpoints functional
- [ ] Search latency < 500ms (p95)
- [ ] Card save latency < 2s (p95)
- [ ] 0 security vulnerabilities
- [ ] 90%+ test coverage

**User Experience:**
- [ ] Create deck + 10 cards in < 5 minutes
- [ ] Semantic search accuracy > 80%
- [ ] Export to GitHub works end-to-end
- [ ] Mobile responsive

**Operational:**
- [ ] $0/month cost (free tier)
- [ ] 99.5% uptime
- [ ] < 5 critical bugs in first week
- [ ] Error rate < 1%

---

## 🔥 Critical Path (Must Complete in Order)

1. ✅ Setup → Database → Backend → Frontend
2. ✅ Backend + Frontend → Semantic Search
3. ✅ Search → Card System → Card Builder
4. ✅ Card Builder → Authentication → Testing
5. ✅ Testing → Deployment

---

## ⚠️ High-Risk Items (Monitor Closely)

- [ ] Transformers.js model loading (22MB download)
- [ ] GitHub API rate limiting (5000/hour)
- [ ] Supabase free tier limits (500MB storage)
- [ ] Embedding quality (384-dim vs 1536-dim)

---

## 📝 Progress Tracking

**Week 1:** [ ] Setup + Database  
**Week 2:** [ ] Backend + Frontend Foundation  
**Week 3:** [ ] Semantic Search + Cards  
**Week 4:** [ ] Card Builder (Part 1)  
**Week 5:** [ ] Card Builder (Part 2) + GitHub  
**Week 6:** [ ] UI Polish + Interactions  
**Week 7:** [ ] Authentication + Testing (Part 1)  
**Week 8:** [ ] Testing (Part 2) + Deployment  
**Week 9-10:** [ ] Desktop Version (Optional)

---

**Current Status:** 🟡 Not Started | 🟢 In Progress | ✅ Complete

**Next Action:** Begin Phase 0 (Project Setup)
