# Quick Start Guide - Phase 3 Testing

## Current Status

✅ Backend server is RUNNING on http://localhost:8000  
✅ Test infrastructure is READY  
❌ Database migration is PENDING (blocking tests)

## What You Need to Do

### Step 1: Run Database Migration (CRITICAL)

1. Open Supabase Dashboard: https://supabase.com/dashboard
2. Select your project
3. Go to: **SQL Editor** (left sidebar)
4. Click: **New Query**
5. Copy contents of: `Backend/migrations/001_initial_schema.sql`
6. Paste and click: **Run**

### Step 2: Verify Migration

Run in SQL Editor:
```sql
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' AND table_name = 'notes';
```

### Step 3: Restart Backend Server

Look for: `✓ Supabase connection verified`

### Step 4: Get Authentication Token

Create test user in Supabase Dashboard or use Auth API

### Step 5: Run Automated Tests

```bash
cd Backend
$env:TOKEN="YOUR_JWT_TOKEN_HERE"
python tests/test_api.py
```

## Quick Links

- **Backend Server:** http://localhost:8000
- **Swagger UI:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health
- **Supabase Dashboard:** https://supabase.com/dashboard

## Files Reference

- **Migration SQL:** `Backend/migrations/001_initial_schema.sql`
- **Test Script:** `Backend/tests/test_api.py`
- **Test README:** `Backend/tests/README.md`
- **Manual Checklist:** `Backend/tests/manual_test_checklist.md`
