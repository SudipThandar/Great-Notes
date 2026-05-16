from fastapi import APIRouter, Depends, status, Query
from typing import List, Optional
from supabase import Client
from app.dependencies import get_current_user, get_user_db_client
from app.schemas.user import UserResponse
from app.schemas.note import NoteCreate, NoteUpdate, NoteResponse
from app.services import note_service


router = APIRouter(prefix="/api/notes", tags=["notes"])


@router.get("", response_model=List[NoteResponse])
async def list_notes(
    search: Optional[str] = Query(None),
    favorites: Optional[bool] = Query(None),
    current_user: UserResponse = Depends(get_current_user),
    supabase: Client = Depends(get_user_db_client)
):
    """List all notes for the current user with optional filters."""
    return await note_service.get_notes(supabase, current_user.id, search, favorites)


@router.get("/trash", response_model=List[NoteResponse])
async def list_trash_notes(
    current_user: UserResponse = Depends(get_current_user),
    supabase: Client = Depends(get_user_db_client)
):
    """List all deleted notes for the current user."""
    return await note_service.get_trash_notes(supabase, current_user.id)


@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(
    note_id: str,
    current_user: UserResponse = Depends(get_current_user),
    supabase: Client = Depends(get_user_db_client)
):
    """Get a single note by ID."""
    return await note_service.get_note_by_id(supabase, note_id, current_user.id)



@router.post("", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(
    note_data: NoteCreate,
    current_user: UserResponse = Depends(get_current_user),
    supabase: Client = Depends(get_user_db_client)
):
    """Create a new note."""
    return await note_service.create_note(supabase, current_user.id, note_data)


@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(
    note_id: str,
    note_data: NoteUpdate,
    current_user: UserResponse = Depends(get_current_user),
    supabase: Client = Depends(get_user_db_client)
):
    """Update an existing note."""
    return await note_service.update_note(supabase, note_id, current_user.id, note_data)


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: str,
    current_user: UserResponse = Depends(get_current_user),
    supabase: Client = Depends(get_user_db_client)
):
    """Soft delete a note (move to trash)."""
    await note_service.delete_note(supabase, note_id, current_user.id)
    return None


@router.post("/{note_id}/restore", response_model=NoteResponse)
async def restore_note(
    note_id: str,
    current_user: UserResponse = Depends(get_current_user),
    supabase: Client = Depends(get_user_db_client)
):
    """Restore a note from trash."""
    return await note_service.restore_note(supabase, note_id, current_user.id)


@router.delete("/{note_id}/permanent", status_code=status.HTTP_204_NO_CONTENT)
async def permanent_delete_note(
    note_id: str,
    current_user: UserResponse = Depends(get_current_user),
    supabase: Client = Depends(get_user_db_client)
):
    """Permanently delete a note from database."""
    await note_service.permanent_delete_note(supabase, note_id, current_user.id)
    return None
