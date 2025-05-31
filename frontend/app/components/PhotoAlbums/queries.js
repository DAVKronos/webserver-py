import { convertToFormData, restCall } from '../../utils/rest-helper'

function getPhotoAlbums () {
  return restCall('photoalbums').then(res => res.data)
}

function getPhotoAlbum (queryKey, id) {
  return restCall(`photoalbums/${id}`).then(res => res.data)
}

function createPhotoAlbum (data) {
  return restCall('photoalbums/', { method: 'POST', data }) // ← no wrapping in "photoalbum"
    .then(res => res.data)
}

function updatePhotoAlbum (id, data) {
  return restCall(`photoalbums/${id}`, { method: 'PUT', data }) // no "photoalbum" wrapper
    .then(res => res.data)
}

function removePhotoAlbum (id) {
  return restCall(`photoalbums/${id}`, { method: 'DELETE' }).then(res => res.data)
}

function getPhotos (queryKey, photoAlbumId) {
  return restCall(`photoalbums/${photoAlbumId}/photos`).then(res => res.data)
}

async function addPhotosToAlbums(photoAlbumId, photos, progressCallBack) {
  const total = photos.length

  for (let idx = 0; idx < total; idx++) {
    const photo = photos[idx]
    const formData = convertToFormData('photo', { photo })

    const onUploadProgress = (e) => {
      if (e.lengthComputable) {
        progressCallBack({ loaded: idx + 0.9 * (e.loaded / e.total), total })
      }
    }

    try {
      await restCall(`photoalbums/${photoAlbumId}/photos`, {
        method: 'POST',
        data: formData,
        onUploadProgress
      })
      progressCallBack({ loaded: idx + 1, total })
    } catch (e) {
      console.error(`❌ Upload failed for photo ${idx + 1}`, e)
    }
  }

  return Promise.resolve()
}

function deletePhoto (photoAlbumId, photoId) {
  return restCall(`photoalbums/${photoAlbumId}/photos/${photoId}`, { method: 'DELETE' }).then(res => res.data)
}



export function addTagToPhoto(photoAlbumId, photoId, tag) {
  return fetch(`/api/v1/photoalbums/${photoAlbumId}/${photoId}/tags`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ tag })
  }).then(async (res) => {
    if (!res.ok) {
      const error = await res.json()
      throw new Error(error.detail || 'Failed to add tag')
    }
    return res.json()
  })
}

export async function getPhotosByTagSearch(tag) {
  const response = await fetch(`/api/v1/photoalbums/photos/search?tag=${encodeURIComponent(tag)}`);
  if (!response.ok) {
    throw new Error('Failed to search photos by tag');
  }
  return response.json();
}


export { getPhotoAlbums, getPhotoAlbum, createPhotoAlbum, updatePhotoAlbum, removePhotoAlbum, getPhotos, addPhotosToAlbums, deletePhoto }
