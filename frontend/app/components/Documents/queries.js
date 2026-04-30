import { restCall, convertToFormData } from '../../utils/rest-helper'

/* ================= FOLDERS ================= */

export function getFolders() {
  return restCall('folders').then(res => res.data)
}

export function getFolderById(_, id) {
  return restCall(`folders/${id}`).then(res => res.data)
}

export function getSubfolders(_, id) {
  return restCall(`folders/${id}/folders`).then(res => res.data)
}

export function getFolderDocuments(_, id) {
  return restCall(`folders/${id}/documents`).then(res => res.data)
}

export function createFolder(data) {
  return restCall('folders', {
    method: 'POST',
    data: { folder: data }
  }).then(res => res.data)
}

export function updateFolder(id, data) {
  return restCall(`folders/${id}`, {
    method: 'PUT',
    data: { folder: data }
  }).then(res => res.data)
}

export function removeFolder(id) {
  return restCall(`folders/${id}`, { method: 'DELETE' })
}

/* ================= DOCUMENTS ================= */

export function getDocuments() {
  return restCall('documents').then(res => res.data)
}

export function getDocumentById(_, id) {
  return restCall(`documents/${id}`).then(res => res.data)
}

export function createDocument(data) {
  const formData = convertToFormData('document', data)
  return restCall('documents', {
    method: 'POST',
    data: formData
  }).then(res => res.data)
}

export function updateDocument(id, data) {
  const formData = convertToFormData('document', data)
  return restCall(`documents/${id}`, {
    method: 'PUT',
    data: formData
  }).then(res => res.data)
}

export function removeDocument(id) {
  return restCall(`documents/${id}`, { method: 'DELETE' })
}