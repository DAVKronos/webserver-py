import { axiosInstance } from './rest-helper'
import { Ability } from '@casl/ability'
import { createCanBoundTo } from '@casl/react'

function getAbilities () {
  return axiosInstance.get('/auth/permissions').then(res => res.data)
}

function updateAbilities (ability) {
  return getAbilities().then(rules => {
    ability.update(rules)
    return rules
  })
}

let authDetails = {}
const ability = new Ability()
const updateAbility = () => { updateAbilities(ability) }

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
    return axiosInstance({method:"post", url:'/auth/login', data: form, headers: {"Content-Type": "multipart/form-data" }})
	    .then((response) => {
        const data = response.data
        if ('access_token' in data) {
          return data.access_token
        }
        return null
    })
}

function logout () {
  return axiosInstance.post('/auth/logout', {})
}

function forgotPassword (email) {
  const host = window && window.location && window.location.host // in case of server side rendering
  const protocol = window && window.location && window.location.protocol // in case of server side rendering
  return axiosInstance.post('/auth/password', { email, redirect_url: `${protocol}//${host}/users/reset_password` })
}

function changePassword (password, password_confirmation) {
  return axiosInstance.put('/auth/password', { password, password_confirmation })
}

function resetPassword (password, password_confirmation, uid, client, access_token) {
  return axiosInstance.put('/auth/password', { password, password_confirmation })
}

const Can = createCanBoundTo(ability)

export {
  login,
  logout,
  ability,
  Can,
  updateAbility,
  getAuthDetails,
  forgotPassword,
  resetPassword,
  changePassword
}
