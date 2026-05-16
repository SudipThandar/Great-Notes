# Great Notes

A modern, full-stack note-taking application with Google OAuth authentication.

## ✨ Features

- 📝 Create, edit, and delete notes
- ⭐ Mark notes as favorites
- 🔍 Search notes by title
- 🗑️ Soft delete with trash functionality
- 🔐 Google OAuth authentication
- 💾 Persistent storage with Supabase
- 🔒 Row Level Security (RLS) for data privacy
- 🎨 Beautiful, responsive UI

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- Supabase account

### 1. Clone and Setup

```bash
git clone <repository-url>
cd Great-Notes
```

### 2. Backend Setup

```bash
cd Backend
python -m venv notes-env
.\notes-env\Scripts\Activate.ps1  # Windows
# or
source notes-env/bin/activate  # Mac/Linux

pip install -r requirements.txt
```

Create `Backend/.env`:
```env
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key
SUPABASE_JWT_SECRET=your-jwt-secret
```

### 3. Frontend Setup

```bash
cd Frontend
npm install
```

Create `Frontend/.env`:
```env
VITE_SUPABASE_URL=your-supabase-url
VITE_SUPABASE_ANON_KEY=your-anon-key
VITE_API_BASE_URL=http://localhost:8000
```

### 4. Database Setup

1. Go to Supabase Dashboard → SQL Editor
2. Run the migration from `Backend/migrations/001_initial_schema.sql`

### 5. Run the Application

**Terminal 1 - Backend:**
```bash
cd Backend
.\notes-env\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd Frontend
npm run dev
```

Visit http://localhost:5173

## 📚 Documentation

- [Startup Guide](STARTUP_GUIDE.md) - Quick start instructions
- [API Documentation](Backend/docs/API.md) - API endpoints reference
- [Supabase Setup](docs/supabase-setup-guide.md) - Database configuration
- [Implementation Status](docs/implementation-status.md) - Project progress

## 🏗️ Tech Stack

### Frontend
- React 18
- React Router
- Supabase JS Client
- Vite

### Backend
- FastAPI
- Supabase (PostgreSQL)
- Python Jose (JWT)
- Pydantic

### Database
- PostgreSQL (via Supabase)
- Row Level Security (RLS)

## 📁 Project Structure

```
Great-Notes/
├── Backend/
│   ├── app/
│   │   ├── routers/      # API endpoints
│   │   ├── services/     # Business logic
│   │   ├── schemas/      # Data models
│   │   ├── database/     # DB connection
│   │   └── middleware/   # Middleware
│   ├── migrations/       # SQL migrations
│   └── tests/           # Tests
├── Frontend/
│   └── src/
│       ├── components/  # React components
│       ├── services/    # API client
│       └── lib/        # Supabase client
└── docs/               # Documentation
```

## 🔐 Security

- JWT-based authentication
- Row Level Security (RLS) policies
- User-specific data isolation
- Secure token handling
- CORS configuration

## 🎯 API Endpoints

- `GET /api/notes` - List notes
- `POST /api/notes` - Create note
- `GET /api/notes/{id}` - Get note
- `PUT /api/notes/{id}` - Update note
- `DELETE /api/notes/{id}` - Delete note
- `GET /api/notes/trash` - List trash
- `POST /api/notes/{id}/restore` - Restore note

Full API docs: http://localhost:8000/docs

## 🧪 Testing

```bash
cd Backend
pytest tests/
```

## 📝 License

MIT

## 👥 Contributing

Contributions welcome! Please read the contributing guidelines first.

---

**Status:** ✅ Fully Functional

Built with ❤️ using FastAPI, React, and Supabase
