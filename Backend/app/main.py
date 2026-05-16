from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.config import settings
from app.routers import auth, notes, share
from app.database.supabase import verify_connection
from app.middleware.request_logger import RequestLoggerMiddleware
from app.middleware.security_headers import SecurityHeadersMiddleware
from app.middleware.error_handler import (
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler
)
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI(
    title="Great Notes API",
    description="Backend API for Great Notes application",
    version="1.0.0"
)

# Add exception handlers
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Add middleware (order matters - last added is executed first)
# 1. Security headers (outermost)
app.add_middleware(SecurityHeadersMiddleware)

# 2. Request logging
app.add_middleware(RequestLoggerMiddleware)

# 3. CORS (innermost, closest to routes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router)
app.include_router(notes.router)
app.include_router(share.router)


@app.on_event("startup")
async def startup_event():
    """Verify Supabase connection on startup."""
    if verify_connection():
        print("✓ Supabase connection verified")
    else:
        print("✗ Supabase connection failed")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "great-notes-api"}
