from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import Client
from jose import jwt, JWTError
from app.database.supabase import get_supabase_client, get_user_supabase_client
from app.config import settings
from app.schemas.user import UserResponse


security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    supabase: Client = Depends(get_supabase_client)
) -> UserResponse:
    """Validate JWT token and return current user."""
    token = credentials.credentials
    
    try:
        # Use Supabase to validate the token directly
        response = supabase.auth.get_user(token)
        
        if not response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        return UserResponse(
            id=response.user.id,
            email=response.user.email,
            created_at=response.user.created_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Authentication error: {str(e)}")  # Debug logging
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )


def get_user_db_client(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Client:
    """Get Supabase client with user's JWT token for RLS."""
    token = credentials.credentials
    return get_user_supabase_client(token)
