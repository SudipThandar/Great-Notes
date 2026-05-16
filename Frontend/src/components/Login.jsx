import {
  Link
} from 'react-router-dom'

export default function Login(){

  return(

    <div className="auth-page">

      <div className="auth-overlay"></div>

      <div className="auth-card">

        <div className="auth-icon">
          ✦
        </div>

        <h1>
          Welcome Back
        </h1>

        <p>
          Continue writing your thoughts.
        </p>

        <input
          type="email"
          placeholder="Enter your email"
        />

        <input
          type="password"
          placeholder="Enter your password"
        />

        <button>
          Login
        </button>

        <span>

          Don’t have an account?

          <Link to="/signup">

            Create one

          </Link>

        </span>

      </div>

    </div>
  )
}