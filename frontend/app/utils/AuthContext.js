import React, { createContext, useState, useEffect, useContext, useCallback } from 'react'
import { ability, updateAbility } from './auth-helper'
import { http, setUnauthorizedHandler } from './rest-helper'
import { getAccessToken, setAccessToken, clearAccessToken } from './token-store'
import queryCache from './query-cache'

export const authContext = createContext({})

function getCurrentUser () {
  return http.get('/auth/current_user').then(res => res.data)
}

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(getAccessToken)
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  // Only hide the app until the *first* auth check is done; later logins/logouts
  // shouldn't unmount the whole tree.
  const [initialized, setInitialized] = useState(false)

  const login = useCallback((newToken, persist = false) => {
    // Write the store before updating state so requests fired by the re-render carry the token.
    setAccessToken(newToken, persist)
    setLoading(true)
    setToken(newToken)
  }, [])

  const logout = useCallback(() => {
    clearAccessToken()
    setToken(null)
  }, [])

  useEffect(() => {
    setUnauthorizedHandler(logout)
  }, [logout])

  useEffect(() => {
    let cancelled = false

    // /auth/permissions requires a login, so anonymous users simply get no rules.
    const resolveUser = token
      ? getCurrentUser().then(async (userData) => {
        await updateAbility()
        return userData
      })
      : Promise.resolve(null)

    resolveUser
      .catch((error) => {
        console.error('Failed to authenticate user:', error)
        logout()
        return null
      })
      .then((userData) => {
        if (cancelled) return
        if (!userData) ability.update([])
        setUser(userData)
        setLoading(false)
        setInitialized(true)
        // Anything fetched under the previous identity may be wrong now.
        queryCache.invalidateQueries()
      })

    return () => { cancelled = true }
  }, [token, logout])

  return (
    <authContext.Provider value={{ token, user, login, logout, loading }}>
      {initialized && children}
    </authContext.Provider>
  )
}

export const useAuth = () => useContext(authContext)
