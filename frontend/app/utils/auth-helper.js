import axios from 'axios'
import { getConfig, restCall } from './rest-helper'
import { Ability } from '@casl/ability'
import { createCanBoundTo } from '@casl/react'
import { jwtDecode } from 'jwt-decode'


function getAbilities () {
  return axios.get(`/auth/permissions`, getConfig()).then(res => res.data)
}

function updateAbilities (ability) {
  return getAbilities().then(rules => {
    ability.update(rules)
    return rules
  })
}

function initializeAbilities () {
  const ability = new Ability()
  updateAbilities(ability)
  return ability
}

function getAuthentication () {
  if (!localStorage.getItem('access_token')) {
    return null
  }
  return JSON.parse(localStorage.getItem('access_token'))
}


let authDetails = {}
const ability = initializeAbilities()

function getAuthDetails () {
  return Object.freeze(authDetails)
}

function setAuthDetails (obj) {
  authDetails = obj
}

function login (email, password, rememberMe) {
    const form = new FormData();
    form.append("username", email)
    form.append("password", password)
    return axios({method:"post", url:'/auth/login', data: form, headers: {"Content-Type": "multipart/form-data" }})
	    .then((response) => {
        const auth_state = {}
        const data = response.data
        if ('access_token' in data) {
          auth_state.access_token = jwtDecode(data.access_token)
          if (rememberMe) {
            localStorage.setItem('access_token', data.access_token)
          }
          setAuthDetails(auth_state)
          return true
        }
         //return updateAbilities(ability).then(() => {
        //  return user
        //})
        return false
    })
}

function logout () {
  return axios.post('/auth/logout', {}, getConfig())
    .then(() => {
      localStorage.removeItem('access_token')
      setAuthDetails(null)
      return updateAbilities(null)
    })
    .catch(() => {
      return undefined
    })
}

function forgotPassword (email) {
  if (localStorage.getItem('kronos-auth')) {
    localStorage.removeItem('kronos-auth')
  }

  const host = window && window.location && window.location.host // in case of server side rendering
  const protocol = window && window.location && window.location.protocol // in case of server side rendering
  return axios.post('/auth/password', { email, redirect_url: `${protocol}//${host}/users/reset_password` }, getConfig())
}

function changePassword (password, password_confirmation) {
  return axios.put('/auth/password', { password, password_confirmation }, getConfig())
}

function resetPassword (password, password_confirmation, uid, client, access_token) {
  const config = getConfig()
  config.headers = { ...config.headers, 'access-token': access_token, uid, client }
  return axios.put('/auth/password', { password, password_confirmation }, config)
}

const Can = createCanBoundTo(ability)

export {
  login,
  logout,
  ability,
  Can,
  getAuthDetails,
  forgotPassword,
  resetPassword,
  changePassword
}
