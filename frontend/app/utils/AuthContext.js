import React, { createContext, useState, useEffect, useContext } from 'react'
import { updateAbility } from './auth-helper'
import { axiosInstance } from './rest-helper'

export const authContext = createContext({})

// FIX: Accept the token parameter and attach it directly to the request headers
function getCurrentUser(token) {
  return axiosInstance.get('/auth/current_user', {
    headers: {
      Authorization: `Bearer ${token}`
    }
  }).then(res => res.data)
}

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(() => localStorage.getItem('access_token'))
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  const login = function(newToken, persist = false) {
    setToken(newToken)
    if (persist) localStorage.setItem('access_token', newToken)
  }
  
  const logout = function() {
    setToken(null)
    setUser(null)
    localStorage.removeItem('access_token')
  }

  useEffect(() => {
    if (token) {
      setLoading(true)
      getCurrentUser(token)
        .then((userData) => {
          setUser(userData)
          return updateAbility()
        })
        .catch((error) => {
          console.error("Failed to authenticate user on refresh:", error)
          logout()
        })
        .finally(() => {
          setLoading(false)
        })
    } else {
      setUser(null)
      updateAbility().finally(() => {
        setLoading(false)
      })
    }
  }, [token])

  

  return (
    <authContext.Provider value={{ token, user, login, logout, loading }}>
      {!loading && children}
    </authContext.Provider>
  )
}

export const useAuth = () => useContext(authContext);