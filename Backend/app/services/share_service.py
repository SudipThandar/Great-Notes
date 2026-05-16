from supabase import Client
import secrets
from app.schemas.note import ShareResponse, SharedNoteResponse
from app.config import settings
from fastapi import HTTPException, status


async def generate_share_token(
    supabase: Client,
    note_id: str,
    user_id: str
) -> ShareResponse:
    """Generate a unique share token for a note."""
    # Verify note exists and belongs to user
    check = supabase.table("notes").select("id").eq("id", note_id).eq("user_id", user_id).execute()
    
    if not check.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    
    # Generate unique token
    max_attempts = 10
    for _ in range(max_attempts):
        token = secrets.token_urlsafe(16)
        
        # Check if token already exists
        existing = supabase.table("notes").select("id").eq("share_token", token).execute()
        
        if not existing.data:
            # Token is unique, update note
            response = supabase.table("notes").update({"share_token": token}).eq("id", note_id).eq("user_id", user_id).execute()
            
            if response.data:
                share_url = f"{settings.share_base_url}/{token}"
                return ShareResponse(share_url=share_url, share_token=token)
    
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Failed to generate unique share token")


async def get_shared_note(
    supabase: Client,
    share_token: str
) -> SharedNoteResponse:
    """Get a note by share token (public access)."""
    response = supabase.table("notes").select("title, content, created_at").eq("share_token", share_token).is_("deleted_at", "null").execute()
    
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shared note not found")
    
    return SharedNoteResponse(**response.data[0])


async def revoke_share(
    supabase: Client,
    note_id: str,
    user_id: str
) -> None:
    """Revoke share access by removing share token."""
    response = supabase.table("notes").update({"share_token": None}).eq("id", note_id).eq("user_id", user_id).execute()
    
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
