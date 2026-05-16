import React from 'react'

import { useState, useEffect } from 'react'

import {
  Routes,
  Route
} from 'react-router-dom'

import Login from './components/Login'
import Signup from './components/Signup'
import AuthCallback from './components/AuthCallback'
import { supabase } from './lib/supabase'
import { notesService } from './services/notes'


function App() {

  const [page, setPage] = useState('home')

  const [notes, setNotes] = useState([])

  const [highGlow, setHighGlow] = useState(true)

  const [search, setSearch] = useState("")

  const [user, setUser] = useState(null)

  const [loading, setLoading] = useState(false)

  const [currentNote, setCurrentNote] = useState({
    id: null,
    title: '',
    content: '',
    favorite: false,
  })

  // Fetch user session on mount
  useEffect(() => {
    // Get initial session
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null)
    })

    // Listen for auth changes
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user ?? null)
    })

    return () => subscription.unsubscribe()
  }, [])

  // Load notes when user logs in
  useEffect(() => {
    if (user) {
      loadNotes()
    } else {
      setNotes([])
    }
  }, [user])

  // Load notes from backend
  const loadNotes = async () => {
    if (!user) return
    
    setLoading(true)
    try {
      const fetchedNotes = await notesService.getNotes()
      const transformedNotes = fetchedNotes.map(note => ({
        id: note.id,
        title: note.title,
        content: note.content,
        favorite: note.is_favorite,
        date: new Date(note.created_at).toLocaleDateString("en-US", {
          month: "long",
          day: "numeric",
          year: "numeric"
        })
      }))
      setNotes(transformedNotes)
    } catch (error) {
      console.error('Failed to load notes:', error)
      alert('Failed to load notes. Please try again.')
    } finally {
      setLoading(false)
    }
  }
  const filteredNotes = notes.filter(note =>

    note.title
      .toLowerCase()
      .includes(search.toLowerCase())

  )

  const toggleGlow = () => {

  setHighGlow(prev => !prev)
}

  const createNewNote = () => {

    setCurrentNote({
      id: null,
      title: '',
      content: '',
      favorite: false,
    })

    setPage('editor')
  }

  const saveNote = async () => {
    if (
      currentNote.title.trim() === '' &&
      currentNote.content.trim() === ''
    ) {
      return
    }

    setLoading(true)
    try {
      if (currentNote.id) {
        // Update existing note
        await notesService.updateNote(currentNote.id, currentNote)
      } else {
        // Create new note
        const newNote = await notesService.createNote(currentNote)
        setCurrentNote(prev => ({
          ...prev,
          id: newNote.id
        }))
      }
      
      // Reload notes from backend
      await loadNotes()
      setPage('notes')
    } catch (error) {
      console.error('Failed to save note:', error)
      alert('Failed to save note. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const toggleFavorite = async () => {
    const newFavoriteState = !currentNote.favorite
    
    // Optimistic update
    setCurrentNote(prev => ({
      ...prev,
      favorite: newFavoriteState,
    }))

    if (currentNote.id) {
      try {
        await notesService.updateNote(currentNote.id, {
          ...currentNote,
          favorite: newFavoriteState
        })
        await loadNotes()
      } catch (error) {
        console.error('Failed to update favorite:', error)
        // Revert on error
        setCurrentNote(prev => ({
          ...prev,
          favorite: !newFavoriteState,
        }))
        alert('Failed to update favorite')
      }
    }
  }

  const deleteNote = async () => {
    if (!currentNote.id) {
      setPage('notes')
      return
    }

    setLoading(true)
    try {
      await notesService.deleteNote(currentNote.id)
      await loadNotes()
      
      setCurrentNote({
        id: null,
        title: '',
        content: '',
        favorite: false,
      })
      
      setPage('notes')
    } catch (error) {
      console.error('Failed to delete note:', error)
      alert('Failed to delete note. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const openNote = (note) => {

  setCurrentNote({
    id: note.id,
    title: note.title,
    content: note.content,
    favorite: note.favorite,
  })

  
}

  return(

  <Routes>

    <Route

      path="/"

      element={(

        <div className="app">

      {/* RAIL */}

      <div className={`rail ${highGlow ? "high-glow" : "low-glow"}`}>

        <button onClick={() => setPage('home')}>
          ⌘
        </button>

        <button onClick={createNewNote}>
          🖋
        </button>

        <button onClick={() => setPage('favorites')}>
          ☆
        </button>

        <button onClick={() => setPage('notes')}>
          🗐
        </button>

        <button onClick={toggleGlow}>
          ◐
        </button>

        <button
          className="plus"
          onClick={createNewNote}
        >
          +
        </button>

      </div>

      {/* HOME */}

      {page === 'home' && (

        <div>

          <button
            className="logo"
            onClick={() => setPage('home')}
          >
            Great Note
          </button>

          <div className="content">

            <div className="hero">

              <h1 className="my-text">
                My
              </h1>

              <h1 className="notes-text">
                notes
              </h1>

              <p className="tagline">
                Capture your thoughts,<br />
                organize your mind,<br />
                create your life.
              </p>

            </div>

          </div>

          <button
            className="profile-card"
           onClick={() => window.location.href='/login'}
          >

            <div className="profile-circle"></div>

            <div>
              <h3>{user?.user_metadata?.full_name || user?.email?.split('@')[0] || 'Guest'}</h3>
              <p>{user?.email || 'Not logged in'}</p>
            </div>

          </button>

        </div>

      )}

      {/* NOTES PAGE */}

      {page === 'notes' && (

        <div className="notes-panel">

          <div className="notes-sidebar">

            <div className="sidebar-top">

              <h2>All Notes</h2>

              <span>{notes.length}</span>

            </div>

            <input
              type="text"
              placeholder="Search notes..."
              className="search-bar"

              value={search}

              onChange={(e) =>
                setSearch(e.target.value)
              }

              onKeyDown={(e) => {

                if (e.key === "Enter") {

                  setSearch(e.target.value)
                }
              }}
            />

            <div className="notes-list">

              {filteredNotes.map(note => (

                <div
                  key={note.id}

                  className={`note-item ${currentNote.id === note.id ? "active" : ""}`}

                  onClick={() => openNote(note)}
                >

                  <div className="note-title-row">

                    <h3>
                      {note.title || 'Untitled Note'}
                    </h3>

                    {note.favorite && (

                      <span className="favorite-star">
                        ⭐
                      </span>

                    )}

                  </div>

                  <p>
                    {note.content.slice(0, 45)}
                  </p>

                </div>

              ))}

            </div>

          </div>

          <div className="note-preview">

            {currentNote.title || currentNote.content ? (

              <>

                <div className="preview-top">

                  <div>

                    <h2>
                      {currentNote.title || "Untitled"}
                    </h2>

                    <p>
                      Preview
                    </p>

                  </div>

                  <div className="preview-icons">

                    <button
                      className="preview-action-btn"

                      onClick={() => {

                        setPage('editor')
                      }}
                    >
                      ✎
                    </button>

                  </div>

                </div>

                <h1 className="preview-title">
                  {currentNote.title}
                </h1>

                <p className="preview-body">
                  {currentNote.content}
                </p>

              </>

            ) : (

              <div className="center-page">

                <h2>No Notes Yet</h2>

              </div>

            )}

          </div>

        </div>

      )}

      {/* EDITOR */}

      {page === 'editor' && (

        <div>

          <button
            className="back-btn"
            onClick={() => setPage('notes')}
          >
            Back
          </button>

          <div className="editor-page">

            <div className="editor-header">

              <div className="editor-title-section">

                <input
                  type="text"
                  placeholder="Untitled Note"
                  className="editor-title"

                  value={currentNote.title}

                  onChange={(e) =>
                    setCurrentNote({
                      ...currentNote,
                      title: e.target.value,
                    })
                  }
                />

                <p className="editor-date">
                   {currentNote.date || "New Note"}
                </p>

              </div>

              <div className="editor-actions">

                <button onClick={toggleFavorite}>
                  {currentNote.favorite ? '⭐' : '☆'}
                </button>

                <button>
                  ✎
                </button>

                <button onClick={deleteNote}>
                  🗑
                </button>

              </div>

            </div>

            <textarea
              className="editor-body"

              placeholder="Start writing your thoughts..."

              value={currentNote.content}

              onChange={(e) =>
                setCurrentNote({
                  ...currentNote,
                  content: e.target.value,
                })
              }
            ></textarea>

          </div>

          <button
            className="save-btn"
            onClick={saveNote}
            disabled={loading}
          >
            {loading ? 'Saving...' : 'Save'}
          </button>

        </div>

      )}

    {page === 'favorites' && (

  <div className="notes-panel">

    <div className="notes-sidebar">

      <div className="sidebar-top">

        <h2>Favorites</h2>

        <span className="notes-count"> {
          notes.filter(
            note => note.favorite
          ).length
        }

        </span>

      </div>

      <input
        type="text"

        placeholder="Search favorites..."

        className="search-bar"

        value={search}

        onChange={(e) =>
          setSearch(e.target.value)
        }
      />

      <div className="notes-list">

        {notes

          .filter(note => note.favorite)

          .filter(note =>

            note.title
              .toLowerCase()
              .includes(
                search.toLowerCase()
              )

          )

          .map(note => (

            <div
              key={note.id}

              className={`note-item ${
                currentNote?.id === note.id
                  ? 'active'
                  : ''
              }`}

              onClick={() => openNote(note)}
            >

              <div className="note-title-row">

                <h3>
                  {note.title || 'Untitled Note'}
                </h3>

                <span className="favorite-star">
                  ⭐
                </span>

              </div>

              <p>
                {
                  note.content ||
                  'Empty note'
                }
              </p>

            </div>

        ))}

      </div>

    </div>

    <div className="note-preview">

      {currentNote ? (

        <>

          <div className="preview-top">

            <div>

              <h2>
                {currentNote.title}
              </h2>

              <p>Preview</p>

            </div>

            <div className="preview-icons">

              <button
                className="preview-action-btn"

                onClick={() => {
                  setPage('editor')
                }}
              >
                ✎
              </button>

            </div>

          </div>

          <h1 className="preview-title">

            {currentNote.title}

          </h1>

          <div className="preview-body">

            {currentNote.content}

          </div>

        </>

      ) : (

        <div className="empty-preview">

          Select a favorite note

        </div>

      )}

    </div>

  </div>

)}

      {/* PROFILE */}

      {page === 'profile' && (

        <div className="center-page">

          <h1>Profile</h1>

          <p>
            Logged in as {user?.user_metadata?.full_name || user?.email || 'Guest'}
          </p>

        </div>

      )}

      
        </div>

      )}

    />

    <Route
      path="/login"
      element={<Login />}
    />

    <Route
      path="/signup"
      element={<Signup />}
    />

    <Route
      path="/auth/callback"
      element={<AuthCallback />}
    />

  </Routes>
)

}
export default App