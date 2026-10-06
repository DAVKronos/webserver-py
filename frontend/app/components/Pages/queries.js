import { restCall } from '../../utils/rest-helper'

function getPage(queryKey, id) {
  return restCall(`pages/${id}`).then(res => res.data)
}

function getPages(queryKey) {
  return restCall('pages').then(res => res.data)
}

function getPageByPageTag(queryKey, page_title_nl) {
  return restCall('pages').then(res => {
    return res.data.find(
      page => page.page_title_nl === page_title_nl
    )
  })
}

function createPage(data) {
  return restCall('pages/', {
    method: 'POST',
    data: data
  }).then(res => res.data)
}

function updatePage(id, data) {
  return restCall(`pages/${id}`, {
    method: 'PATCH',
    data: data
  }).then(res => res.data)
}

function removePage(id) {
  return restCall(`pages/${id}`, {
    method: 'DELETE'
  }).then(res => res.data)
}

export { getPage, getPages, getPageByPageTag, createPage, updatePage, removePage }