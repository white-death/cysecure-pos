import { useState } from 'react'

import logo from '../assets/elan-logo.png'

import '../styles/login.css'


function LoginCard() {

  const [username, setUsername] = useState('')

  const [password, setPassword] = useState('')

  const [loading, setLoading] = useState(false)

  const handleLogin = async (e) => {

    e.preventDefault()

    setLoading(true)

    try {

      const response = await fetch(
        'http://192.168.0.119:8000/auth/login',
        {
          method: 'POST',

          headers: {
            'Content-Type': 'application/json'
          },

          body: JSON.stringify({
            username,
            password
          })
        }
      )

      const data = await response.json()

      console.log(data)

      if (!response.ok) {

        alert('Invalid Username or Password')

        setLoading(false)

        return

      }

      localStorage.setItem(
        'access_token',
        data.access_token
      )

      localStorage.setItem(
        'refresh_token',
        data.refresh_token
      )

      localStorage.setItem(
        'token_type',
        data.token_type
      )

      alert('Login Successful')

      window.location.href = '/dashboard'

    } catch (err) {

      console.error(err)

      alert('Server Error')

    } finally {

      setLoading(false)

    }

  }

  return (

    <div className="login-page">

      <img
        src={logo}
        alt="Elan-Nexum PoS"
        className="login-logo"
      />

      <div className="login-card">

        <div className="login-header">

          <h1 className="login-title">

            Elan-Nexum PoS

          </h1>

          <p className="login-subtitle">

            Secure Access Portal

          </p>

        </div>

        <form
          onSubmit={handleLogin}
          className="login-form"
        >

          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="login-input"
            required
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="login-input"
            required
          />

          <button
            type="submit"
            className="login-button"
            disabled={loading}
          >

            {
              loading
                ? 'Authenticating...'
                : 'Login'
            }

          </button>

        </form>

      </div>

    </div>

  )

}

export default LoginCard
