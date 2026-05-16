from fastapi import APIRouter, Depends, status
from app.dependencies import get_current_user
from app.schemas.user import UserResponse


router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: UserResponse = Depends(get_current_user)
):
    """Get current authenticated user information."""
    return current_user


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout():
    """Logout endpoint (token removal handled client-side)."""
    return None
