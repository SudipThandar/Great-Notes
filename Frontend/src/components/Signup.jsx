import {
  Link
} from 'react-router-dom'
import { supabase } from '../lib/supabase'

export default function Signup(){

  const handleGoogleSignIn = async () => {
    try {
      const { error } = await supabase.auth.signInWithOAuth({
        provider: 'google',
        options: {
          redirectTo: `${window.location.origin}/auth/callback`,
          queryParams: {
            access_type: 'offline',
            prompt: 'consent',
          },
        },
      })
      
      if (error) {
        console.error('Google sign-in error:', error.message)
        alert('Failed to sign in with Google: ' + error.message)
      }
    } catch (err) {
      console.error('Unexpected error:', err)
      alert('An unexpected error occurred')
    }
  }

  return(

    <div className="auth-page">

      <div className="auth-overlay"></div>

      <div className="auth-card">

        <div className="auth-icon">
          ✦
        </div>

        <h1>
          Create Account
        </h1>

        <p>
          Start your journey of beautiful thoughts.
        </p>

        <input
          type="text"
          placeholder="Full name"
        />

        <input
          type="email"
          placeholder="Enter your email"
        />

        <input
          type="password"
          placeholder="Create password"
        />

        <button>
          Create Account
        </button>

        <div className="auth-divider">
          <span>or</span>
        </div>

        <button className="google-btn" onClick={handleGoogleSignIn}>
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M19.8055 10.2292C19.8055 9.55056 19.7501 8.86667 19.6306 8.19861H10.2002V12.0492H15.6014C15.3773 13.2911 14.6571 14.3898 13.6025 15.0875V17.5866H16.8251C18.7173 15.8449 19.8055 13.2728 19.8055 10.2292Z" fill="#4285F4"/>
            <path d="M10.2002 20.0006C12.9516 20.0006 15.2727 19.1151 16.8296 17.5865L13.607 15.0874C12.7096 15.6972 11.5521 16.0428 10.2047 16.0428C7.54356 16.0428 5.28656 14.2828 4.48516 11.9165H1.16406V14.4923C2.75766 17.8695 6.31176 20.0006 10.2002 20.0006Z" fill="#34A853"/>
            <path d="M4.48065 11.9163C4.06065 10.6744 4.06065 9.33093 4.48065 8.08905V5.51318H1.16405C-0.387951 8.66905 -0.387951 12.3353 1.16405 15.4912L4.48065 11.9163Z" fill="#FBBC04"/>
            <path d="M10.2002 3.95805C11.6248 3.93555 13.0042 4.47305 14.0361 5.45805L16.8933 2.60055C15.1827 0.990547 12.9337 0.0768134 10.2002 0.104313C6.31176 0.104313 2.75766 2.23555 1.16406 5.61305L4.48066 8.18893C5.27756 5.81805 7.53906 3.95805 10.2002 3.95805Z" fill="#EA4335"/>
          </svg>
          Continue with Google
        </button>

        <span>

          Already have an account?

          <Link to="/login">

            Sign in

          </Link>

        </span>

      </div>

    </div>
  )
}