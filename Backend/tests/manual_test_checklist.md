# Manual Test Checklist for Great Notes Backend

**Prerequisites:**
- Backend server running on http://localhost:8000
- Supabase project configured with database migration run
- Valid access token from Google OAuth

## Setup

1. **Run Database Migration:**
   - Go to Supabase Dashboard > SQL Editor
   - Copy contents of `Backend/migrations/001_initial_schema.sql`
   - Execute the SQL
   - Verify `notes` table exists

2. **Start Backend Server:**
   ```bash
   cd Backend
   notes-env\Scripts\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   - Verify server starts without errors
   - Check for "✓ Supabase connection verified" message

3. **Get Authentication Token:**
   - Option A: Use Swagger UI at http://localhost:8000/docs
   - Option B: Use curl commands below with a valid JWT token
   - To get a token: Login via frontend or use Supabase Auth API

4. **Set Environment Variable for Testing:**
   ```bash
   # Replace with your actual token
   $TOKEN = "your_jwt_token_here"
   ```

---

## 1. Authentication Tests

- [ ] GET /api/auth/me with valid token returns user info
- [ ] GET /api/auth/me with invalid token returns 401
- [ ] GET /api/auth/me without token returns 401
- [ ] POST /api/auth/logout returns 204

## 2. Notes CRUD Tests

- [ ] POST /api/notes creates note successfully
- [ ] GET /api/notes returns only current user's notes
- [ ] GET /api/notes excludes deleted notes
- [ ] GET /api/notes/{id} returns note if owned
- [ ] GET /api/notes/{id} returns 404 for other user's note
- [ ] PUT /api/notes/{id} updates note successfully
- [ ] PUT /api/notes/{id} returns 404 for other user's note
- [ ] DELETE /api/notes/{id} soft deletes note
- [ ] Deleting already-deleted note succeeds (idempotent)

## 3. Search and Filter Tests

- [ ] GET /api/notes?search=test filters by title (case-insensitive)
- [ ] GET /api/notes?favorites=true returns only favorites
- [ ] GET /api/notes?search=test&favorites=true combines filters
- [ ] Empty search returns all notes

## 4. Trash Tests

- [ ] GET /api/notes/trash returns only deleted notes
- [ ] POST /api/notes/{id}/restore clears deleted_at
- [ ] DELETE /api/notes/{id}/permanent removes from database
- [ ] DELETE /api/notes/{id}/permanent returns 400 if not in trash

## 5. Share Tests

- [ ] POST /api/notes/{id}/share generates unique token
- [ ] POST /api/notes/{id}/share returns share_url
- [ ] GET /api/share/{token} returns note without auth
- [ ] GET /api/share/{token} returns 404 for deleted notes
- [ ] GET /api/share/{token} returns 404 for invalid token
- [ ] DELETE /api/notes/{id}/share clears token

## 6. RLS Security Tests

- [ ] User A cannot access User B's notes
- [ ] User A cannot update User B's notes
- [ ] User A cannot delete User B's notes
- [ ] Public can access shared notes
- [ ] Deleted shared notes return 404

## 7. Error Handling Tests

- [ ] Invalid JSON returns 422
- [ ] Missing required fields returns 422
- [ ] Invalid UUID returns 422
- [ ] Title >500 chars returns 422
- [ ] Content >50000 chars returns 422
- [ ] Server errors return 500

## 8. Middleware Tests

- [ ] CORS headers present in responses
- [ ] X-Content-Type-Options header present
- [ ] X-Frame-Options header present
- [ ] X-Process-Time header present
- [ ] Request logging works

## 9. Health Check Tests

- [ ] GET /health returns 200
- [ ] GET /health works without authentication
- [ ] Server logs "Supabase connection verified" on startup

## 10. API Documentation Tests

- [ ] http://localhost:8000/docs loads (Swagger UI)
- [ ] http://localhost:8000/redoc loads
- [ ] All endpoints listed in docs
- [ ] Try it out feature works

---

## Test Summary

**Passed:** _____ / _____
**Failed:** _____ / _____

**Issues Found:**
1. 
2. 
3. 

**Tester:** _______________
**Date:** _______________
