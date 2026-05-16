import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { supabase } from '../lib/supabase'

export default function AuthCallback() {
  const navigate = useNavigate()

  useEffect(() => {
    // Handle the OAuth callback
    const handleCallback = async () => {
      try {
        // Get the session from the URL
        const { data: { session }, error } = await supabase.auth.getSession()
        
        if (error) {
          console.error('Auth callback error:', error)
          alert('Authentication failed: ' + error.message)
          navigate('/signup')
          return
        }

        if (session) {
          console.log('Authentication successful!', session.user)
          // Redirect to the main app
          navigate('/')
        } else {
          console.log('No session found')
          navigate('/signup')
        }
      } catch (err) {
        console.error('Unexpected error in auth callback:', err)
        navigate('/signup')
      }
    }

    handleCallback()
  }, [navigate])

  return (
    <div className="auth-page">
      <div className="auth-overlay"></div>
      <div className="auth-card">
        <div className="auth-icon">✦</div>
        <h1>Completing sign in...</h1>
        <p>Please wait while we log you in.</p>
      </div>
    </div>
  )
}
