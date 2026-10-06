import { restCall, convertToFormData } from '../../utils/rest-helper'

function getUserCommittees (querykey, userId) {
  return restCall(`users/${userId}/committees`).then((res) => res.data)
}
function getUsers (queryKey) {
  return restCall('users').then((res) => res.data)
}

function getUser (queryKey, id) {
  return restCall(`users/${id}`).then((res) => res.data)
}

function getUserType (queryKey, id) {
  return restCall(`user_types/${id}`).then((res) => res.data)
}

function getUserTypes () {
  return restCall('user_types').then((res) => res.data)
}

function createUser (data) {
  const formData = convertToFormData('user', data)
  return restCall('users', {
    method: 'POST',
    data: formData
  }).then((res) => res.data)
}

function updateUser (id, data) {
  const { avatar, ...otherFields} = data
  return restCall(`users/${id}`, {
    method: 'PATCH',
    data: otherFields,
  }).then((res) => {
    // If an avatar file was chosen, upload the file
    if (avatar && avatar instanceof File) {
      const formData = new FormData()
      formData.append('avatar', avatar)

      return restCall(`users/${id}/avatar`, {
        method: 'POST',
        data: formData,
        headers: { 'Content-Type': 'multipart/form-data' }
      }).then((avatarRes) => avatarRes.data)
    }
    return res.data
  })
}

function removeUser (id) {
  return restCall(`users/${id}`, { method: 'DELETE' })
}

export {
  getUserCommittees,
  getUser,
  getUsers,
  getUserType,
  getUserTypes,
  createUser,
  updateUser,
  removeUser
}
