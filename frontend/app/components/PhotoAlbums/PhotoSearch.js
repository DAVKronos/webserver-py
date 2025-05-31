import React, { useState } from 'react'
import { Form, Button, Row, Col, Card, Badge, Alert } from 'react-bootstrap'
import { useTranslation } from 'react-i18next'
import { Link } from 'react-router-dom'
import { useQuery } from 'react-query'
import axios from 'axios'

function PhotoSearch() {
  const { t } = useTranslation('generic')
  const [searchTerm, setSearchTerm] = useState('')
  const [searchTrigger, setSearchTrigger] = useState('')
  const [error, setError] = useState(null)

  const { data: photos, isLoading } = useQuery(
    ['photo-search', searchTrigger],
    async () => {
      if (!searchTrigger) return []
      const res = await axios.get(`/api/v1/photoalbums/photos/search`, {
        params: { tag: searchTrigger }
      })
      return res.data
    },
    {
      enabled: !!searchTrigger, // Only run query when search is triggered
      onError: (err) => setError(err.message || 'Failed to fetch')
    }
  )

  const handleSearch = (e) => {
    e.preventDefault()
    const trimmed = searchTerm.trim()
    if (trimmed) {
      setSearchTrigger(trimmed)
      setError(null)
    }
  }

  return (
    <div>
      <h1>{t('Search photos')}</h1>

      <Form onSubmit={handleSearch} className='mb-4'>
        <Form.Control
          type='text'
          placeholder={t('search_tag')}
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <Button type='submit' className='mt-2'>{t('search')}</Button>
      </Form>

      {error && <Alert variant='danger'>{error}</Alert>}
      {isLoading && <p>{t('loading')}...</p>}

      <Row>
        {(photos || []).map((photo, idx) => (
          <Col key={idx} md={3} className='mb-4'>
            <Card>
              <Link to={`/photoalbums/${photo.photoalbum_id}/${photo.id}`}>
                <Card.Img
                  variant='top'
                  src={`/static/photos/${photo.photo_url_thumb?.split('/').pop()}`}
                  alt={photo.caption}
                />
              </Link>
              <Card.Body>
                <Card.Text>{photo.caption}</Card.Text>
                <div>
                  {(photo.tags || []).map((tag, i) => (
                    <Badge key={i} className='mr-1' variant='light'>
                      {tag}
                    </Badge>
                  ))}
                </div>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>
    </div>
  )
}

export default PhotoSearch
