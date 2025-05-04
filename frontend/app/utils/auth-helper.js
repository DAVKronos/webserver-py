import axios from 'axios'
import { getConfig, restCall } from './rest-helper'
import { Ability } from '@casl/ability'
import { createCanBoundTo } from '@casl/react'

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
        const data = response.data
        if ('access_token' in data) {
          return data.access_token
        }
        return null
    })
}

function logout () {
  return axios.post('/auth/logout', {}, getConfig())
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
