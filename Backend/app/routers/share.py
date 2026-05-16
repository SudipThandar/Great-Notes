from fastapi import APIRouter, Depends, status
from supabase import Client
from app.dependencies import get_current_user, get_supabase_client
from app.schemas.user import UserResponse
from app.schemas.note import ShareResponse, SharedNoteResponse
from app.services import share_service


router = APIRouter(tags=["share"])


@router.post("/api/notes/{note_id}/share", response_model=ShareResponse)
async def generate_share_link(
    note_id: str,
    current_user: UserResponse = Depends(get_current_user),
    supabase: Client = Depends(get_supabase_client)
):
    """Generate a public share link for a note."""
    return await share_service.generate_share_token(supabase, note_id, current_user.id)


@router.delete("/api/notes/{note_id}/share", status_code=status.HTTP_204_NO_CONTENT)
async def revoke_share_link(
    note_id: str,
    current_user: UserResponse = Depends(get_current_user),
    supabase: Client = Depends(get_supabase_client)
):
    """Revoke public share access for a note."""
    await share_service.revoke_share(supabase, note_id, current_user.id)
    return None


@router.get("/api/share/{share_token}", response_model=SharedNoteResponse)
async def get_shared_note(
    share_token: str,
    supabase: Client = Depends(get_supabase_client)
):
    """Get a shared note by token (public, no authentication required)."""
    return await share_service.get_shared_note(supabase, share_token)
