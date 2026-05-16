# Great Notes - Quick Startup Guide

## ✅ What's Already Done

- ✅ Backend code complete
- ✅ Frontend UI complete
- ✅ Supabase project created
- ✅ Backend .env configured
- ✅ Frontend .env configured
- ✅ Python dependencies installed
- ✅ Frontend dependencies installed

## ⚠️ Critical Step: Run Database Migration

**You MUST do this before starting the servers!**

1. Go to: https://supabase.com/dashboard/project/jgzhumfjsntxscohzada
2. Click **SQL Editor** in the left sidebar
3. Click **New Query**
4. Open `Backend/migrations/001_initial_schema.sql` in your editor
5. Copy the entire SQL content
6. Paste it into the Supabase SQL Editor
7. Click **Run** (or press Ctrl+Enter)
8. You should see: "Success. No rows returned"

## 🚀 Starting the Servers

### Terminal 1 - Backend Server

```bash
cd Backend
.\notes-env\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

Backend will run at: **http://localhost:8000**
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### Terminal 2 - Frontend Server

```bash
cd Frontend
npm run dev
```

Frontend will run at: **http://localhost:5173**

## 🧪 Testing the Application

### 1. Test Backend API
Open http://localhost:8000/docs to see all API endpoints

### 2. Test Frontend
1. Open http://localhost:5173
2. Click "Sign in with Google"
3. Complete Google OAuth flow
4. You should be redirected back to the app

### 3. Basic Functionality Test
- Create a new note
- Edit the note
- Mark as favorite
- Delete note (moves to trash)
- Restore from trash
- Share a note

## ⚠️ Important Notes

### Backend is Ready ✅
The backend API is fully functional and can be tested immediately after running the migration.

### Frontend Needs API Integration ⚠️
The frontend UI is complete but **NOT connected to the backend yet**. It currently uses local state only.

**Frontend integration work needed (4-5 hours):**
- Create API service layer (`Frontend/src/services/api.js`)
- Create auth service (`Frontend/src/services/auth.js`)
- Create notes service (`Frontend/src/services/notes.js`)
- Update all components to use API instead of local state
- Add loading states and error handling

See `Backend/docs/FRONTEND_INTEGRATION.md` for detailed integration guide.

## 📚 Documentation

- **API Documentation**: `Backend/docs/API.md`
- **Frontend Integration Guide**: `Backend/docs/FRONTEND_INTEGRATION.md`
- **Supabase Setup**: `docs/supabase-setup-guide.md`
- **Backend README**: `Backend/README.md`
- **Test Checklist**: `Backend/tests/manual_test_checklist.md`

## 🐛 Troubleshooting

### Backend won't start
- Make sure virtual environment is activated
- Check `.env` file has correct Supabase credentials
- Verify database migration was run

### Frontend won't start
- Run `npm install` in Frontend folder
- Check `.env` file exists with Supabase credentials

### "Table 'notes' not found" error
- You forgot to run the database migration!
- Go back to the "Run Database Migration" section above

### Google OAuth not working
- Check Supabase Dashboard > Authentication > Providers
- Verify Google OAuth is enabled
- Check redirect URLs are configured

## 📊 Current Status

**What Works Now:**
- ✅ Backend API (after migration)
- ✅ Frontend UI (local state only)
- ✅ Google OAuth (via Supabase)

**What Doesn't Work Yet:**
- ❌ Frontend → Backend communication
- ❌ Data persistence in frontend
- ❌ Real note CRUD operations in frontend

**Next Steps:**
1. Run database migration
2. Start both servers
3. Test backend API with Swagger UI
4. Test frontend UI (will use local state)
5. Implement frontend API integration (see FRONTEND_INTEGRATION.md)

---

**Estimated Time to Full Functionality:**
- Database migration: 5 minutes
- Backend testing: 30 minutes
- Frontend API integration: 4-5 hours
- **Total: ~5 hours**
