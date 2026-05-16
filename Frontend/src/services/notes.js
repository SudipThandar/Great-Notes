import { apiClient } from './api'

/**
 * Notes service - handles all note-related API calls
 */
export const notesService = {
  /**
   * Get all notes (with optional filters)
   */
  async getNotes(filters = {}) {
    const params = new URLSearchParams()
    
    if (filters.search) {
      params.append('search', filters.search)
    }
    
    if (filters.favorites) {
      params.append('favorites', 'true')
    }
    
    const query = params.toString()
    const endpoint = query ? `/api/notes?${query}` : '/api/notes'
    
    return apiClient.get(endpoint)
  },

  /**
   * Get a single note by ID
   */
  async getNote(noteId) {
    return apiClient.get(`/api/notes/${noteId}`)
  },

  /**
   * Create a new note
   */
  async createNote(noteData) {
    return apiClient.post('/api/notes', {
      title: noteData.title || '',
      content: noteData.content || '',
      is_favorite: noteData.favorite || false,
    })
  },

  /**
   * Update an existing note
   */
  async updateNote(noteId, noteData) {
    return apiClient.put(`/api/notes/${noteId}`, {
      title: noteData.title,
      content: noteData.content,
      is_favorite: noteData.favorite,
    })
  },

  /**
   * Delete a note (soft delete - moves to trash)
   */
  async deleteNote(noteId) {
    return apiClient.delete(`/api/notes/${noteId}`)
  },

  /**
   * Get trash notes
   */
  async getTrashNotes() {
    return apiClient.get('/api/notes/trash')
  },

  /**
   * Restore a note from trash
   */
  async restoreNote(noteId) {
    return apiClient.post(`/api/notes/${noteId}/restore`, {})
  },

  /**
   * Permanently delete a note
   */
  async permanentDeleteNote(noteId) {
    return apiClient.delete(`/api/notes/${noteId}/permanent`)
  },

  /**
   * Generate a share link for a note
   */
  async shareNote(noteId) {
    return apiClient.post(`/api/notes/${noteId}/share`, {})
  },

  /**
   * Revoke share link for a note
   */
  async unshareNote(noteId) {
    return apiClient.delete(`/api/notes/${noteId}/share`)
  },

  /**
   * Get a shared note by token (public, no auth required)
   */
  async getSharedNote(token) {
    const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
    const response = await fetch(`${API_BASE_URL}/api/share/${token}`)
    
    if (!response.ok) {
      throw new Error('Failed to fetch shared note')
    }
    
    return response.json()
  },
}
