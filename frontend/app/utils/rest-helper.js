import axios from 'axios'
import { getAccessToken } from './token-store'

const API_HOST = '/api/v1'

// The one HTTP client for the whole app. Use `restCall` for /api/v1 endpoints
// and `http` directly for the few routes outside it (/auth/...).
const http = axios.create({
  headers: { Accept: 'application/json' }
})

http.interceptors.request.use((config) => {
  const token = getAccessToken()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

let onUnauthorized = () => {}

// Called once by AuthContext so an expired/invalid token logs the user out.
function setUnauthorizedHandler (handler) {
  onUnauthorized = handler
}

http.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401 && getAccessToken()) {
      onUnauthorized()
    }
    return Promise.reject(error)
  }
)

function convertToFormData (objectName, data) {
  const formData = new FormData()
  Object.keys(data).forEach((field) => {
    if (data[field] !== undefined && data[field] !== null) {
      formData.append(`${objectName}[${field}]`, data[field])
    }
  })
  return formData
}

// restCall('newsitems'), restCall(`newsitems/${id}`, { method: 'PATCH', data }), ...
function restCall (url, params = {}, method = 'get') {
  return http.request({ method, ...params, url: `${API_HOST}/${url}` })
}

export {
  http,
  restCall,
  API_HOST,
  convertToFormData,
  setUnauthorizedHandler
}
