import {
  Link
} from 'react-router-dom'

export default function Signup(){

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