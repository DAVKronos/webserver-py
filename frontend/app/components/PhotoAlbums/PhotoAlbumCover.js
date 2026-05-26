import React, { useState } from 'react'
import { Button, Card } from 'react-bootstrap'
import { Link, useHistory } from 'react-router-dom'
import { format } from '../../utils/date-format'
import DefaultSpinner from '../Generic/Spinner'
import { useQuery, useQueryCache } from 'react-query'
import { getPhotos, removePhotoAlbum } from './queries'
import { subject } from '@casl/ability'
import { Can } from '../../utils/auth-helper'
import { useTranslation } from 'react-i18next'
import placeholder from '../../images/image-thumb-placeholder.png'

const PhotoAlbumCover = ({ photoAlbum }) => {
  const id = photoAlbum.id
  const queryCache = useQueryCache()
  const { t, i18n } = useTranslation('generic')
  const lang = i18n.language
  const { isLoading, isError, data: photos, error } = useQuery(['photos', id], getPhotos)
  const [isImageLoaded, setIsImageLoaded] = useState(false)

  const hasThumbnail = photos && photos[0] && photos[0].thumbnail_file

  const onClickRemove = () => {
    removePhotoAlbum(id).then(() => {
      return queryCache.invalidateQueries('photoalbums')
    })
  }
  const name = lang === 'nl' ? photoAlbum.name_nl : photoAlbum.name_en
  return (
    <Card style={{ marginBottom: 10 }}>
      {(!hasThumbnail || (isLoading && !isImageLoaded)) && <Card.Img variant='top' src={""} />}
      {(isLoading && !isImageLoaded) && <Card.ImgOverlay><DefaultSpinner /></Card.ImgOverlay>}
      {hasThumbnail && <Card.Img
        variant='top'
        className={isImageLoaded ? 'd-block' : 'd-none'}
        src={`/${photos[0].thumbnail_file.path}`}
        onLoad={() => setIsImageLoaded(true)}
                     />}
      <Card.Body>
        <Card.Title><Link to={`/photoalbums/${photoAlbum.id}`}>{name}</Link></Card.Title>
        <Card.Text>
          {photoAlbum.created_at && format(photoAlbum.created_at, 'PPP p', lang)}
        </Card.Text>
        <Can I='edit' this={subject('Photoalbum', photoAlbum)}>
          <Button size='sm' variant='warning' as={Link} to={`/photoalbums/${id}/edit`}>
            {t('edit')}
          </Button>
        </Can>
        <Can I='delete' this={subject('Photoalbum', photoAlbum)}>
          <Button size='sm' variant='danger' onClick={() => onClickRemove(photoAlbum.id)}>
            {t('remove')}
          </Button>
        </Can>
      </Card.Body>
    </Card>
  )
}

export default PhotoAlbumCover
