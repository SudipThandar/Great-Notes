# Backend Testing Guide

This directory contains testing resources for the Great Notes Backend API.

## Prerequisites

Before running tests, ensure:

1. **Database Migration Executed**
   - Go to Supabase Dashboard > SQL Editor
   - Copy and execute `Backend/migrations/001_initial_schema.sql`
   - Verify the `notes` table exists

2. **Backend Server Running**
   ```bash
   cd Backend
   notes-env\Scripts\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   - Check for "✓ Supabase connection verified" message
   - Server should be accessible at http://localhost:8000

3. **Valid JWT Token**
   - Option A: Login via frontend and copy token from localStorage
   - Option B: Use Supabase Auth API to generate a token
   - Option C: Use Swagger UI at http://localhost:8000/docs

## Running Automated Tests

### Install Dependencies

```bash
pip install requests
```

### Run Tests

**With token as argument:**
```bash
python tests/test_api.py --token YOUR_JWT_TOKEN_HERE
```

**With token as environment variable:**
```bash
# Windows PowerShell
$env:TOKEN="YOUR_JWT_TOKEN_HERE"
python tests/test_api.py

# Windows CMD
set TOKEN=YOUR_JWT_TOKEN_HERE
python tests/test_api.py
```

**Without token (limited tests):**
```bash
python tests/test_api.py
```
Note: Only health check and unauthenticated tests will run.

### Test Output

The script will:
- Run 7 test suites with 30+ test cases
- Display colored output (✓ PASS / ✗ FAIL)
- Show detailed error messages for failures
- Print a summary with pass/fail counts
- Exit with code 0 (success) or 1 (failure)

### Test Suites

1. **Health Check Tests** - Verify server is running
2. **Authentication Tests** - Test JWT validation and auth endpoints
3. **Notes CRUD Tests** - Test create, read, update, delete operations
4. **Search and Filter Tests** - Test search and favorites filtering
5. **Trash Operations Tests** - Test soft delete, restore, permanent delete
6. **Sharing Tests** - Test share link generation and public access
7. **Error Handling Tests** - Test invalid inputs and error responses

## Manual Testing

For manual testing, use the checklist in `manual_test_checklist.md`.

### Using Swagger UI

1. Open http://localhost:8000/docs
2. Click "Authorize" button
3. Enter: `Bearer YOUR_JWT_TOKEN`
4. Click "Authorize" and "Close"
5. Test endpoints by clicking "Try it out"

### Using curl

```bash
# Set token variable
TOKEN="YOUR_JWT_TOKEN_HERE"

# Health check (no auth required)
curl http://localhost:8000/health

# Get current user
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/auth/me

# Create a note
curl -X POST http://localhost:8000/api/notes \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Note","content":"Test content","is_favorite":false}'

# Get all notes
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/notes
```

## Troubleshooting

### Server Won't Start

**Error: "ModuleNotFoundError: No module named 'supabase'"**
- Solution: Activate virtual environment and install dependencies

**Error: "Supabase connection failed"**
- Solution: Run database migration in Supabase SQL Editor
- Check `.env` file has correct Supabase credentials

### Tests Failing

**401 Unauthorized errors**
- Token expired: Generate a new token
- Token invalid: Check token format (should be JWT)
- Token not set: Verify TOKEN environment variable

**404 Not Found errors**
- Database migration not run: Execute `001_initial_schema.sql`
- RLS policies blocking access: Check Supabase RLS settings

**Connection errors**
- Server not running: Start backend server
- Wrong URL: Verify server is on http://localhost:8000

## Test Coverage

Current test coverage includes:

- ✅ Health check endpoint
- ✅ Authentication (valid/invalid/missing tokens)
- ✅ Notes CRUD (create, read, update, delete)
- ✅ Search by title (case-insensitive)
- ✅ Filter by favorites
- ✅ Soft delete (trash)
- ✅ Restore from trash
- ✅ Permanent delete
- ✅ Share link generation
- ✅ Public share access (no auth)
- ✅ Share revocation
- ✅ Error handling (invalid JSON, invalid UUIDs)
- ✅ HTTP status codes
- ✅ Response formats

## Next Steps

After all tests pass:

1. Review test results and fix any failures
2. Test RLS policies with multiple users
3. Perform security testing
4. Test with frontend integration
5. Proceed to Phase 4 (Bug Fixes) if issues found
6. Proceed to Phase 5 (Final Verification) when stable
