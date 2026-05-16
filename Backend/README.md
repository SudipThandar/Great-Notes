# Great Notes Backend

FastAPI backend for the Great Notes application with Supabase integration.

## Features

- Google OAuth authentication via Supabase
- Note CRUD operations with search and favorites
- Soft delete with trash/restore functionality
- Public note sharing via unique URLs
- Row Level Security (RLS) for data isolation

## Tech Stack

- **Framework:** FastAPI 0.109.0
- **Database:** Supabase (PostgreSQL)
- **Authentication:** Supabase Auth (Google OAuth)
- **Language:** Python 3.10+

## Setup Instructions

### 1. Prerequisites

- Python 3.10 or higher
- Supabase account and project
- Google OAuth credentials

### 2. Create Virtual Environment

```bash
python -m venv notes-env
source notes-env/bin/activate  # On Windows: notes-env\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

Required variables:
- `SUPABASE_URL` - Your Supabase project URL
- `SUPABASE_KEY` - Your Supabase anon key
- `SUPABASE_SERVICE_KEY` - Your Supabase service role key
- `SUPABASE_JWT_SECRET` - Your Supabase JWT secret


### 5. Set Up Database

1. Go to your Supabase project dashboard
2. Navigate to SQL Editor
3. Run the migration file: `migrations/001_initial_schema.sql`
4. Verify the `notes` table and RLS policies are created

### 6. Configure Google OAuth

1. In Supabase dashboard, go to Authentication > Providers
2. Enable Google provider
3. Add your Google OAuth client ID and secret
4. Configure redirect URLs (e.g., `http://localhost:5173/auth/callback`)

### 7. Run the Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

## API Endpoints

### Authentication
- `GET /api/auth/me` - Get current user info
- `POST /api/auth/logout` - Logout (204 response)

### Notes CRUD
- `GET /api/notes` - List notes (with search, favorites filters)
- `GET /api/notes/{id}` - Get single note
- `POST /api/notes` - Create note
- `PUT /api/notes/{id}` - Update note
- `DELETE /api/notes/{id}` - Soft delete note

### Trash
- `GET /api/notes/trash` - List deleted notes
- `POST /api/notes/{id}/restore` - Restore from trash
- `DELETE /api/notes/{id}/permanent` - Permanent delete

### Sharing
- `POST /api/notes/{id}/share` - Generate share link
- `DELETE /api/notes/{id}/share` - Revoke share
- `GET /api/share/{token}` - Get shared note (public, no auth)

## Project Structure

```
Backend/
├── app/
│   ├── main.py              # FastAPI app entry
│   ├── config.py            # Settings and environment variables
│   ├── dependencies.py      # Auth middleware
│   ├── routers/             # API endpoints
│   │   ├── auth.py
│   │   ├── notes.py
│   │   └── share.py
│   ├── services/            # Business logic
│   │   ├── note_service.py
│   │   └── share_service.py
│   ├── schemas/             # Pydantic models
│   │   ├── note.py
│   │   └── user.py
│   └── database/            # Database client
│       └── supabase.py
├── migrations/              # Database migrations
├── tests/                   # Test files
├── requirements.txt         # Python dependencies
└── .env.example            # Environment template
```

## Development

### Testing

Run manual tests using the checklist:
```bash
cat tests/manual_test_checklist.md
```

### Troubleshooting

**Connection Issues:**
- Verify Supabase URL and keys in `.env`
- Check if Supabase project is active
- Ensure RLS policies are enabled

**Authentication Errors:**
- Verify JWT secret matches Supabase project
- Check token format in Authorization header
- Ensure Google OAuth is configured in Supabase

**Database Errors:**
- Verify migration was run successfully
- Check RLS policies are active
- Ensure user_id references are correct

## Security

- All endpoints (except public share) require JWT authentication
- Row Level Security (RLS) enforces data isolation at database level
- Share tokens are cryptographically secure (16 bytes)
- CORS configured to allow only specified origins

## License

MIT
