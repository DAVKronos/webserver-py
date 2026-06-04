import { restCall } from '../../utils/rest-helper'

// ----------------------
// NEWS ITEMS
// ----------------------

function getNewsItem(queryKey, id) {
  return restCall(`newsitems/${id}`).then(res => res.data)
}

function getUnapprovedNewsItem(queryKey, id) {
  return restCall(`newsitems/unapproved/${id}`).then(res => res.data)
}

function getNewsItems(queryKey, params = null) {
  return restCall('newsitems').then(res => res.data)
}

function createNewsItem(data) {
  return restCall('newsitems', {
    method: 'POST',
    data
  }).then(res => res.data)
}

function updateNewsItem(id, data) {
  return restCall(`newsitems/${id}`, {
    method: 'PUT',
    data
  }).then(res => res.data)
}

function removeNewsItem(id) {
  return restCall(`newsitems/${id}`, {}, 'delete').then(res => res.data)
}

function approveNewsItem(id) {
  return restCall(`newsitems/${id}/agreed`, {
    method: 'POST'
  }).then(res => res.data)
}

// ----------------------
// COMMENTS
// ----------------------

function getNewsItemComments(queryKey, newsItemId) {
  return restCall(`newsitems/${newsItemId}/comments`).then(res => res.data)
}

function createNewsItemComment(newsItemId, data) {
  return restCall(`newsitems/${newsItemId}/comments`, {
    method: 'POST',
    data
  }).then(res => res.data)
}

function removeNewsItemComment(newsItemId, id) {
  return restCall(
    `newsitems/${newsItemId}/comments/${id}`,
    {},
    'delete'
  ).then(res => res.data)
}

// ----------------------
// EXPORTS
// ----------------------

export {
  getNewsItem,
  getUnapprovedNewsItem,
  getNewsItems,
  createNewsItem,
  updateNewsItem,
  removeNewsItem,
  approveNewsItem,
  getNewsItemComments,
  createNewsItemComment,
  removeNewsItemComment
}