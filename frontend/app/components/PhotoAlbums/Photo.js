import React, { useState, useEffect } from 'react'
import {
  Button, ButtonGroup, Col, Form, Image,
  Row, Badge, InputGroup
} from 'react-bootstrap'
import { Link, NavLink } from 'react-router-dom'
import { useQuery, useMutation } from 'react-query'
import { getPhotoAlbum, getPhotos, addTagToPhoto } from './queries'
import { useTranslation } from 'react-i18next'
import DefaultSpinner from '../Generic/Spinner'

// Load Google Font
const injectFont = () => {
  const link = document.createElement('link')
  link.href = 'https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap'
  link.rel = 'stylesheet'
  document.head.appendChild(link)
}

function Photo(props) {
  let { photo_id, album_id } = props.match.params
  const { t } = useTranslation('generic')
  const [newTag, setNewTag] = useState('')
  const [localTags, setLocalTags] = useState([])

  useEffect(() => {
    injectFont()
    document.body.style.fontFamily = "'Inter', sans-serif"
  }, [])

  // Reset localTags on photo change
  useEffect(() => {
    setLocalTags([])
  }, [photo_id])

  const { isLoading: albumLoading, data: photoAlbum } = useQuery(['photoalbums', album_id], getPhotoAlbum)
  const { isLoading: photosLoading, data: photos } = useQuery(['photos', album_id], getPhotos)

  const [addTag, { isLoading: isAddingTag }] = useMutation(
    ({ photoId, albumId, tag }) => addTagToPhoto(albumId, photoId, tag),
    {
      onSuccess: (data, variables) => {
        setLocalTags(prev => [...prev, { name: variables.tag }])
        setNewTag('')
      },
      onError: (err) => {
        alert(err.message || 'Error adding tag')
      }
    }
  )

  if (albumLoading || photosLoading) return <DefaultSpinner />
  if (!photoAlbum || !photos) return null

  photo_id = parseInt(photo_id)
  const photoIndex = photos.findIndex(item => item.id === photo_id)
  if (photoIndex < 0) return <h3>{t('not_found')}</h3>

  const photo = photos[photoIndex]
  const prevPhoto = photoIndex > 0 ? photos[photoIndex - 1] : photo
  const nextPhoto = photoIndex < photos.length - 1 ? photos[photoIndex + 1] : photo

  const handleAddTag = () => {
    const trimmedTag = newTag.trim()
    if (trimmedTag !== '') {
      addTag({ photoId: photo.id, albumId: album_id, tag: trimmedTag })
    }
  }

  const combinedTags = [...(photo.tags || []), ...localTags]

  return (
    <div className='photo-container' style={{ fontFamily: "'Inter', sans-serif" }}>
      <Row>
        <Col>
          <h1 style={{ fontWeight: '600', fontSize: '2rem' }}>{photoAlbum.name}</h1>
          <p style={{ color: '#666', marginBottom: '1rem' }}>{photoAlbum.date}</p>
        </Col>
      </Row>

      <Row>
        <Col className='photo'>
          <Image
            src={`/${photo.file.path}`}
            fluid
            style={{ borderRadius: '12px', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}
          />
        </Col>
      </Row>

      {/* <Row className='row-margin mt-4'>
        <Col>
          {combinedTags.length > 0 && (
            <>
              <div style={{ marginBottom: '10px', fontWeight: '500' }}>{t('Tags')}:</div>
              <div style={{ marginBottom: '1rem' }}>
                {combinedTags.map((tag, index) => (
                  <Badge
                    key={index}
                    variant='secondary'
                    style={{
                      marginRight: '8px',
                      padding: '0.5em 0.75em',
                      borderRadius: '20px',
                      fontSize: '0.85rem',
                      backgroundColor: '#f0f0f0',
                      color: '#333'
                    }}
                  >
                    {tag.name || tag}
                  </Badge>
                ))}
              </div>
            </>
          )}

          <InputGroup>
            <Form.Control
              type='text'
              placeholder={t('add_tag')}
              value={newTag}
              onChange={(e) => setNewTag(e.target.value)}
              style={{ borderRadius: '20px 0 0 20px' }}
            />
            <InputGroup.Append>
              <Button
                onClick={handleAddTag}
                disabled={isAddingTag}
                style={{
                  borderRadius: '0 20px 20px 0',
                  backgroundColor: '#333',
                  borderColor: '#333'
                }}
              >
                {t('add')}
              </Button>
            </InputGroup.Append>
          </InputGroup>
        </Col>
      </Row> */}

      <Row className='row-margin mt-4'>
        <Col className='photo-buttons'>
          <Button as={Link} to={`/photoalbums/${album_id}`} variant='outline-dark'>
            {t('back')}
          </Button>
          <ButtonGroup className='ml-2'>
            <Button
              disabled={photoIndex === 0}
              as={NavLink}
              to={`/photoalbums/${album_id}/${prevPhoto.id}`}
              variant='dark'
            >
              {t('previous')}
            </Button>
            <Button
              disabled={photoIndex === photos.length - 1}
              as={NavLink}
              to={`/photoalbums/${album_id}/${nextPhoto.id}`}
              variant='dark'
            >
              {t('next')}
            </Button>
          </ButtonGroup>
        </Col>
      </Row>
    </div>
  )
}

export default Photo
