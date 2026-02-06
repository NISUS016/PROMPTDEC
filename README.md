# PromptDec - TCG-Style Prompt Gallery

**A personal prompt library styled as a trading card game with semantic search, cross-platform support, and GitHub integration.**

[![Status](https://img.shields.io/badge/status-in_development-yellow)]()
[![License](https://img.shields.io/badge/license-MIT-blue)]()

---

## 🎯 Project Overview

PromptDec lets you organize, search, and customize prompt cards across multiple decks. Key features:

- ✨ **Semantic Search** - Find prompts by context, not keywords (Transformers.js)
- 🎴 **TCG-Style Cards** - 3D flip animations, customizable templates
- 📦 **Multi-Deck Organization** - Decks as folders, cards as notes
- 🔄 **GitHub Integration** - Share and sync decks via GitHub
- 🖥️ **Cross-Platform** - Web (Vercel) + Desktop (Tauri)
- 💰 **Zero Cost** - Runs on free tiers ($0/month)

---

## 📚 Documentation

- **[Implementation Roadmap](./IMPLEMENTATION_ROADMAP.md)** - Detailed 8-week plan with 350+ tasks
- **[Quick Checklist](./QUICK_CHECKLIST.md)** - High-level progress tracking
- **[Architecture Evolution](./ARCHITECTURE_EVOLUTION.md)** - V1 vs V2 comparison
- **[Gap Analysis](./GAP_ANALYSIS_SUMMARY.md)** - Executive summary

---

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm/pnpm
- Python 3.10+
- Git
- Supabase account (free tier)

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/promptdec.git
cd promptdec

# Install dependencies
npm install
pip install -r requirements.txt

# Set up environment
cp .env.example .env.local
# Edit .env.local with your Supabase credentials

# Start development servers
npm run dev              # Frontend (port 5173)
python -m uvicorn main:app --reload  # Backend (port 8000)
```

---

## 🏗️ Project Structure

```
promptdec/
├── apps/
│   ├── web/              # Vite + React frontend
│   └── backend/          # FastAPI backend
├── docs/                 # Documentation
├── .env.example          # Environment template
├── README.md
└── package.json
```

---

## 🛠️ Tech Stack

### Frontend
- **Framework:** React 18 + Vite
- **Styling:** Tailwind CSS + Shadcn/UI
- **State:** React Query + Zustand
- **Animations:** Framer Motion
- **Search:** Transformers.js (client-side embeddings)

### Backend
- **Framework:** FastAPI (Python)
- **Database:** PostgreSQL (Supabase) + pgvector
- **Auth:** GitHub OAuth (Supabase Auth)
- **Storage:** Supabase Storage

### DevOps
- **Web:** Vercel (auto-deploy)
- **Backend:** Railway/Render (free tier)
- **Monitoring:** Sentry (error tracking)

---

## 📅 Development Timeline

**Current Phase:** Phase 0 - Project Setup  
**Status:** ✅ In Progress  
**Target MVP:** 8 weeks (full-time) or 12-16 weeks (part-time)

### Roadmap

- [x] Phase 0: Project Setup (Week 1)
- [ ] Phase 1A: Database Schema (Week 1)
- [ ] Phase 1B: Backend Core (Week 2)
- [ ] Phase 1C: Frontend Foundation (Week 2)
- [ ] Phase 2A: Semantic Search (Week 3)
- [ ] Phase 2B: Card System (Week 3-4)
- [ ] Phase 3A: Card Builder (Week 4-5)
- [ ] Phase 3B: GitHub Integration (Week 5)
- [ ] Phase 4: UI Polish (Week 6)
- [ ] Phase 5: Auth + Testing (Week 7)
- [ ] Phase 6: Deployment (Week 8)

---

## 🤝 Contributing

This is currently a personal project. Contributions will be welcome after MVP launch.

---

## 📄 License

MIT License - See [LICENSE](./LICENSE) for details

---

## 🙏 Acknowledgments

- Architecture inspired by Obsidian, Anki, and Pokemon TCG
- Built with guidance from Gemini AI (Antigravity)

---

**Current Status:** 🟡 Phase 0 - Setting up project foundation  
**Next Steps:** Database schema design → Backend API → Frontend setup

---

For detailed implementation guidance, see [IMPLEMENTATION_ROADMAP.md](./IMPLEMENTATION_ROADMAP.md)
