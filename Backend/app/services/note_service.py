from supabase import Client
from typing import List, Optional
from datetime import datetime
from app.schemas.note import NoteCreate, NoteUpdate, NoteResponse
from fastapi import HTTPException, status


async def get_notes(
    supabase: Client,
    user_id: str,
    search: Optional[str] = None,
    favorites: Optional[bool] = None
) -> List[NoteResponse]:
    """Get all notes for a user with optional filters."""
    query = supabase.table("notes").select("*").eq("user_id", user_id).is_("deleted_at", "null")
    
    if search:
        query = query.ilike("title", f"%{search}%")
    
    if favorites:
        query = query.eq("is_favorite", True)
    
    query = query.order("updated_at", desc=True)
    
    response = query.execute()
    return [NoteResponse(**note) for note in response.data]


async def get_note_by_id(
    supabase: Client,
    note_id: str,
    user_id: str
) -> NoteResponse:
    """Get a single note by ID."""
    response = supabase.table("notes").select("*").eq("id", note_id).eq("user_id", user_id).execute()
    
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    
    return NoteResponse(**response.data[0])


async def create_note(
    supabase: Client,
    user_id: str,
    note_data: NoteCreate
) -> NoteResponse:
    """Create a new note."""
    data = {
        "user_id": user_id,
        "title": note_data.title,
        "content": note_data.content,
        "is_favorite": note_data.is_favorite
    }
    
    response = supabase.table("notes").insert(data).execute()
    
    if not response.data:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create note")
    
    return NoteResponse(**response.data[0])


async def update_note(
    supabase: Client,
    note_id: str,
    user_id: str,
    note_data: NoteUpdate
) -> NoteResponse:
    """Update an existing note."""
    # Check if note exists and belongs to user
    await get_note_by_id(supabase, note_id, user_id)
    
    # Build update data
    update_data = {}
    if note_data.title is not None:
        update_data["title"] = note_data.title
    if note_data.content is not None:
        update_data["content"] = note_data.content
    if note_data.is_favorite is not None:
        update_data["is_favorite"] = note_data.is_favorite
    
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")
    
    response = supabase.table("notes").update(update_data).eq("id", note_id).eq("user_id", user_id).execute()
    
    if not response.data:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update note")
    
    return NoteResponse(**response.data[0])


async def delete_note(
    supabase: Client,
    note_id: str,
    user_id: str
) -> None:
    """Soft delete a note (set deleted_at timestamp)."""
    response = supabase.table("notes").update({"deleted_at": datetime.utcnow().isoformat()}).eq("id", note_id).eq("user_id", user_id).execute()
    
    if not response.data:
        # Check if note exists
        check = supabase.table("notes").select("id").eq("id", note_id).eq("user_id", user_id).execute()
        if not check.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")


async def get_trash_notes(
    supabase: Client,
    user_id: str
) -> List[NoteResponse]:
    """Get all deleted notes for a user."""
    response = supabase.table("notes").select("*").eq("user_id", user_id).not_.is_("deleted_at", "null").order("deleted_at", desc=True).execute()
    
    return [NoteResponse(**note) for note in response.data]


async def restore_note(
    supabase: Client,
    note_id: str,
    user_id: str
) -> NoteResponse:
    """Restore a note from trash."""
    response = supabase.table("notes").update({"deleted_at": None}).eq("id", note_id).eq("user_id", user_id).execute()
    
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    
    return NoteResponse(**response.data[0])


async def permanent_delete_note(
    supabase: Client,
    note_id: str,
    user_id: str
) -> None:
    """Permanently delete a note from database."""
    # Check if note is in trash
    check = supabase.table("notes").select("deleted_at").eq("id", note_id).eq("user_id", user_id).execute()
    
    if not check.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    
    if check.data[0]["deleted_at"] is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Note must be in trash before permanent deletion")
    
    supabase.table("notes").delete().eq("id", note_id).eq("user_id", user_id).execute()
