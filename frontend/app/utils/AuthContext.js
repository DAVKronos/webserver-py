import React, { createContext, useState, useEffect, useContext } from 'react'
import { jwtDecode } from 'jwt-decode'
import { updateAbility} from './auth-helper'
import { axiosInstance } from './rest-helper'

export const authContext = createContext({})

function getCurrentUser() {
  return axiosInstance.get('/auth/current_user').then(res => {
    const user = res.data
    return user
  })
}

export const AuthProvider = ({ children }) => {
  // Auth provider manages persistence of the access token, 
  // making that e.g. login function further downstream doesn't need to deal with those details.
  const [token, setToken] = useState(null) 
  const [user, setUser] = useState(null) 
  const [loading, setLoading] = useState(true)


  const login = function(token, persist=false) {
    setToken(token);
    if (persist) localStorage.setItem('access_token', token);
  }
  const logout = function() {
    setToken(null);
    localStorage.removeItem('access_token');
  }

  useEffect(() => {
    const storedToken = localStorage.getItem('access_token');
    if (storedToken && !token) {
      setToken(storedToken);
    }
  }, []);


  useEffect(() => {
    // Update current user after updating the access token.
    if (token !== null) {
      getCurrentUser().then((user) => {
        setUser(user)
      }).catch((error) => {
          console.log(error)
          localStorage.removeItem('access_token')
          setUser(null)
      }).finally(() => {
        setLoading(false)
      })   
    } 
    else {
      if(user !== null) {
      // Only null the user if it is currently set.
      setUser(null)
      }
      setLoading(false)
    }
    updateAbility()
  }, [token])


  return (
    <authContext.Provider value={{ token, user, login, logout }}>
      {!loading && children}
    </authContext.Provider>
  )
}

export const useAuth = () => useContext(authContext);