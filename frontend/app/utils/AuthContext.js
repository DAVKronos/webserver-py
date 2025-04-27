import React, { createContext, useState, useEffect } from 'react'
import { jwtDecode } from 'jwt-decode'
import {  } from './auth-helper'
import axios from 'axios'
import { getConfig } from './rest-helper'

export const authContext = createContext({})


async function getUser () {
  // TODO: don't make he request if you don't have a valid access token anyways
  return axios.get('/auth/current_user', getConfig()).then(res => {
    const user = res.data
    return user
  })
}

function getAuthentication () {
  if (!localStorage.getItem('access_token')) {
    return null
  }
  return jwtDecode(localStorage.getItem('access_token'))
}


const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  const setUserData = (user) => {
    setUser(user)
  }

  useEffect(() => {
    getUser().then((user) => {
      setUser(user)
    }).catch((error) => {
        console.log(error)
        localStorage.removeItem('access_token')
        setUser(null)
    }).finally(() => {
      setLoading(false)
    })

  }, [])

  return (
    <authContext.Provider value={{ user, setUserData }}>
      {!loading && children}
    </authContext.Provider>
  )
}

export default AuthProvider
