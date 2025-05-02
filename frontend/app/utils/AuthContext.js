import React, { createContext, useState, useEffect } from 'react'
import { jwtDecode } from 'jwt-decode'
import {  } from './auth-helper'
import axios from 'axios'
import { getConfig } from './rest-helper'

export const authContext = createContext({})


async function read_current_user() {
  // TODO: don't make he request if you don't have a valid access token anyways
  return axios.get('/auth/current_user', getConfig()).then(res => {
    const user = res.data
    return user
  })
}

function authFromLocalStorage () {
  try {
    return jwtDecode(localStorage.getItem('access_token'))
  }
  catch(e) {
    console.log(e)
    localStorage.removeItem('access_token')
    return null
  }
}
const initial_auth = authFromLocalStorage();

const AuthProvider = ({ children }) => {
  // Auth provider manages persistence of the access token, 
  // making that e.g. login function further downstream doesn't need to deal with those details.
  
  const [auth, setAuthInner] = useState(initial_auth) 
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)


  const setAuth = function(token, persist=false) {
    try {
      setAuthInner(jwtDecode(token))
      if (persist) localStorage.setItem('access_token', token)
    }
    catch (e) {
      setAuthInner(null)
      localStorage.removeItem('access_token')
    }
  }

  useEffect(() => {
    // Update current user after updating the access token.
    if (auth !== null) {
      read_current_user().then((user) => {
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
  }, [auth])

  const setUserData = (user) => {
    setUser(user)
  }

  return (
    <authContext.Provider value={{ auth, setAuth, user, setUser }}>
      {!loading && children}
    </authContext.Provider>
  )
}

export default AuthProvider
