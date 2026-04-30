import { restCall, convertToFormData } from '../../utils/rest-helper'

function getDocuments (queryKey) {
  return restCall('documents/').then((res) => res.data)
}

function getFolders (queryKey) {
  return restCall('folders').then((res) => res.data)
}

function getFolderById (queryKey, folder_id) {
  return restCall(`folders/${folder_id}`).then((res) => res.data)
}

function getDocumentsByFolder (queryKey, folder_id) {
  return restCall(`folders/${folder_id}/documents`).then((res) => res.data)
}

function getDocumentById (queryKey, documentId) {
  return restCall(`documents/${documentId}`).then((res) => res.data)
}

function createFolder (data) {
  return restCall('folders', {
    method: 'POST',
    data: { folder: data }
  }).then((res) => res.data)
}

function updateFolder (id, data) {
  return restCall(`folders/${id}`, {
    method: 'PUT',
    data: { folder: data }
  }).then((res) => res.data)
}

function removeFolder (id) {
  return restCall(`folders/${id}`, { method: 'DELETE' })
}

function createDocument (data) {
  const formData = convertToFormData('document', data)
  return restCall('documents', {
    method: 'POST',
    data: formData
  }).then((res) => res.data)
}

function updateDocument (id, data) {
  const formData = convertToFormData('document', data)
  return restCall(`documents/${id}`, {
    method: 'PUT',
    data: formData
  }).then((res) => res.data)
}

function removeDocument (id) {
  return restCall(`documents/${id}`, { method: 'DELETE' })
}

export {
  getDocuments,
  getFolders,
  getFolderById,
  getDocumentsByFolder,
  getDocumentById,
  createFolder,
  updateFolder,
  removeFolder,
  createDocument,
  updateDocument,
  removeDocument
}
