# PromptDec Setup Guide

**Phase 0 Complete!** ✅ 

Your project foundation is ready. Follow these steps to complete the setup.

---

## ✅ What's Been Created

1. **Git Repository** - Initialized with .gitignore
2. **Project Structure** - apps/web, apps/backend, migrations
3. **Configuration Files** - .env.example, package.json, requirements.txt
4. **Database Schema** - migrations/001_initial_schema.sql
5. **Backend Skeleton** - FastAPI app with health check
6. **Frontend Template** - Vite + React (in apps/web)

---

## 📋 Next Steps

### Step 1: Install Dependencies (5 minutes)

```bash
# Install backend dependencies
cd apps/backend
pip install -r requirements.txt

# Install frontend dependencies  
cd ../web
npm install

# Return to root
cd ../..
```

### Step 2: Set Up Supabase (10 minutes)

1. Go to [supabase.com](https://supabase.com) and create account
2. Create new project (free tier)
3. Go to **Settings** → **API** and copy:
   - Project URL
   - Anon/Public Key
   - Service Role Key (keep secret!)

4. Go to **SQL Editor** and run:
   - `migrations/001_initial_schema.sql`
   - `migrations/002_seed_default_templates.sql`

5. Go to **Authentication** → **Providers** → Enable **GitHub**

### Step 3: Configure Environment Variables (5 minutes)

**Backend (.env in apps/backend/):**
```bash
cd apps/backend
cp .env.example .env
# Edit .env with your Supabase credentials
```

**Frontend (.env.local in apps/web/):**
```bash
cd apps/web
cp ../.env.example .env.local
# Edit .env.local with your Supabase credentials
```

### Step 4: Test Setup (2 minutes)

**Backend:**
```bash
cd apps/backend
python main.py
# Visit http://localhost:8000/health
# Should see: {"status": "healthy", ...}
```

**Frontend:**
```bash
cd apps/web
npm run dev
# Visit http://localhost:5173
# Should see Vite + React welcome page
```

---

## 🎯 Verification Checklist

- [ ] Backend runs on http://localhost:8000
- [ ] Frontend runs on http://localhost:5173
- [ ] /health endpoint returns "healthy"
- [ ] Supabase database has all tables
- [ ] 4 default templates seeded
- [ ] No errors in console

---

## 🚀 What's Next?

You're ready for **Phase 1B: Backend Development**!

Next tasks:
1. Create database connection (SQLAlchemy)
2. Add authentication middleware
3. Build CRUD endpoints for decks
4. Build CRUD endpoints for cards

See `IMPLEMENTATION_ROADMAP.md` → Phase 1B for detailed steps.

---

## 🆘 Troubleshooting

**Backend won't start:**
- Check Python version: `python --version` (need 3.10+)
- Check all dependencies installed: `pip list`
- Check DATABASE_URL in .env

**Frontend won't start:**
- Check Node version: `node --version` (need 18+)
- Delete node_modules and reinstall: `rm -rf node_modules && npm install`

**Database errors:**
- Verify Supabase credentials in .env
- Check SQL migrations ran successfully in Supabase SQL Editor
- Enable RLS policies in Supabase dashboard

---

**Phase 0 Status:** ✅ **COMPLETE**  
**Next Phase:** Phase 1A → Database Schema (deploy to Supabase)  
**Time to MVP:** 7-8 weeks remaining
