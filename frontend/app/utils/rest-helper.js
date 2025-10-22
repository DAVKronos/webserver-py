import axios from 'axios'

const axiosInstance = axios.create({
    baseURL: '/',
});

const API_HOST = '/api/v1'

const config = {
  headers: { Accept: 'application/json' }
}

function convertToFormData (objectName, data) {
  const formData = new FormData()
  Object.keys(data).forEach((field) => {
    if (data[field] != undefined || data[field] != null) {
      formData.append(`${objectName}[${field}]`, data[field])
    }
  })
  return formData
}

function filterJson(data) {
  const filteredJson = {};

  Object.keys(data).forEach((field) => {
    const value = data[field];

    if (value !== undefined && value !== null) {
      if (typeof value === 'string') {
        filteredJson[field] = value.trim() || null;
      } else {
        filteredJson[field] = value;
      }
    }
  });

  return filteredJson;
}




function getAuthHeader () {
  const token = localStorage.getItem("access_token");
  if (token !== null) {
    return {"Authorization": `Bearer ${token}`}
  }
  else {
    return {}
  }
}

function getConfig () {
  const cfg = { ...config }
  cfg.headers = { ...cfg.headers, ...getAuthHeader() }

  return cfg
}

function restCall (url, params = {}, method = 'get') {
  return axios.request({ ...getConfig(), url: `${API_HOST}/${url}`, method, ...params })
}

function getAPIHostUrl (url) {
  return url
}

export {
  axiosInstance,
  restCall,
  API_HOST,
  getAPIHostUrl,
  getConfig,
  convertToFormData,
  filterJson
}
