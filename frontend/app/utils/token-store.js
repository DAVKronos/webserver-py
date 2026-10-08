// Single source of truth for the access token. The axios interceptor in
// rest-helper.js reads it on every request; AuthContext writes it on login/logout.
//
// "Remember me" -> localStorage (survives closing the browser),
// otherwise -> sessionStorage (survives a reload, gone when the tab closes).

const KEY = 'access_token'

let accessToken = localStorage.getItem(KEY) || sessionStorage.getItem(KEY)

function getAccessToken () {
  return accessToken
}

function setAccessToken (token, persist = false) {
  accessToken = token
  localStorage.removeItem(KEY)
  sessionStorage.removeItem(KEY)
  if (token) {
    (persist ? localStorage : sessionStorage).setItem(KEY, token)
  }
}

function clearAccessToken () {
  setAccessToken(null)
}

export { getAccessToken, setAccessToken, clearAccessToken }
