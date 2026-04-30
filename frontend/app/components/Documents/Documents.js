import React, { useState } from 'react'
import { Row, Col, Card, Button, Container, Alert } from 'react-bootstrap'
import { Link, useHistory } from 'react-router-dom'
import {
  getDocumentsByFolder,
  getDocuments,
  getFolders,
  getFolderById,
  removeFolder,
  removeDocument
} from './queries'
import { useQuery, useQueryCache } from 'react-query'
import { useTranslation } from 'react-i18next'
import DefaultSpinner from '../Generic/Spinner'
import { BsFolder, BsArrowUp, BsFileText, BsExclamationTriangle } from 'react-icons/bs'
import { Can } from '../../utils/auth-helper'


const EditFolderButtons = ({ folderId }) => {
  const [removing, setRemoving] = useState(false)
  const history = useHistory()
  const { t } = useTranslation('generic')

  if (!folderId) return null

  const onClickRemove = async () => {
    if (!window.confirm(t('confirmDeleteFolder', 'Are you sure you want to delete this folder?'))) return
    setRemoving(true)
    try {
      await removeFolder(folderId)
      history.push('/documents')
    } catch (err) {
      console.error('Failed to delete folder:', err)
      alert(t('errorDeletingFolder', 'Failed to delete folder.'))
    } finally {
      setRemoving(false)
    }
  }

  return (
    <Col style={{ display: 'flex', alignItems: 'flex-end', justifyContent: 'end' }}>
      <Can I='update' a='Folder'>
        <Button variant='warning' disabled={removing} size='sm' as={Link} to={`/folders/${folderId}/edit`} className='me-2'>
          {t('edit', 'Edit')}
        </Button>
      </Can>
      <Can I='delete' a='Folder'>
        <Button variant='danger' disabled={removing} size='sm' onClick={onClickRemove}>
          {removing ? <DefaultSpinner inline size='sm' /> : t('remove', 'Delete')}
        </Button>
      </Can>
    </Col>
  )
}

const documentCard = ({ document, onRemove, t }) => {
  const [removing, setRemoving] = useState(false)

  // 🔍 Safe data extraction with fallbacks
  const title = document.name || document.title || document.file_name || t('untitled', 'Untitled Document')
  const dateStr = document.date 
    ? new Date(document.date).toLocaleDateString() 
    : t('noDate', 'No date')
  
  // Image & link fallbacks
  const thumbUrl = document.url_thumb || document.thumbnail || document.preview_url || '/placeholder-thumb.jpg'
  const originalUrl = document.url_original || document.url || document.download_url || '#'

  const handleRemove = async () => {
    if (!window.confirm(t('confirmDeleteDoc', 'Delete this document?'))) return
    setRemoving(true)
    try {
      await onRemove(document.id)
    } catch (err) {
      console.error('Delete failed:', err)
      alert(t('errorDeletingDoc', 'Failed to delete document.'))
    } finally {
      setRemoving(false)
    }
  }

  return (
    <Col key={document.id} md={3} sm={4} className="mb-4">
      <Card className="h-100 shadow-sm">
        {originalUrl && originalUrl !== '#' && (
          <a href={originalUrl} target="_blank" rel="noopener noreferrer" className="text-decoration-none">
            <Card.Img 
              variant="top" 
              src={thumbUrl} 
              alt={title}
              onError={(e) => { e.target.src = '/placeholder-thumb.jpg' }}
              style={{ height: '180px', objectFit: 'cover' }}
            />
          </a>
        )}
        <Card.Body className="d-flex flex-column">
          <Card.Title className="h6">
            <Link to={`/documents/${document.id}`} className="text-decoration-none text-dark">
              <BsFileText className="me-2 text-primary" />
              {title}
            </Link>
          </Card.Title>
          <Card.Subtitle className="mb-3 text-muted small">{dateStr}</Card.Subtitle>
          
          <div className="mt-auto d-flex gap-2">
            <Can I='update' a='document'>
              <Button size="sm" variant="warning" as={Link} to={`/documents/${document.id}/edit`}>
                {t('edit', 'Edit')}
              </Button>
            </Can>
            <Can I='delete' a='document'>
              <Button size="sm" variant="danger" onClick={handleRemove} disabled={removing}>
                {removing ? <DefaultSpinner inline size="sm" /> : t('remove', 'Delete')}
              </Button>
            </Can>
          </div>
        </Card.Body>
      </Card>
    </Col>
  )
}

const documents = (props) => {
  const queryCache = useQueryCache()
  const { t } = useTranslation('documentPage')
  const history = useHistory()
  const [debug, setDebug] = useState(false) // Toggle to inspect API response shape

  const folderId = props.match?.params?.folder_id ? parseInt(props.match.params.folder_id) : null

  let folderName, folders, isFolderLoading, documents, isdocumentLoading, parentId, queryError

  if (!folderId) {
    const folderQuery = useQuery('folders', getFolders)
    const documentQuery = useQuery('documents', getDocuments)

    isFolderLoading = folderQuery.isLoading
    folderName = t('mainFolder', 'All Documents')
    folders = folderQuery.data || []
    
    documents = documentQuery.data || []
    isdocumentLoading = documentQuery.isLoading
    queryError = folderQuery.error || documentQuery.error
  } else {
    // ✅ Fix: Wrap to correctly pass folderId as 2nd argument to your query functions
    const folderQuery = useQuery(['folders', folderId], () => getFolderById(null, folderId))
    const documentQuery = useQuery(['folders', folderId, 'documents'], () => getDocumentsByFolder(null, folderId))

    isFolderLoading = folderQuery.isLoading

    if (folderQuery.data) {
      folderName = folderQuery.data.name || folderQuery.data.title || t('unnamedFolder', 'Unnamed Folder')
      folders = folderQuery.data.folders || folderQuery.data.subfolders || []
      parentId = folderQuery.data.folder_id || folderQuery.data.parent_id
    }

    documents = documentQuery.data || []
    isdocumentLoading = documentQuery.isLoading
    queryError = folderQuery.error || documentQuery.error
  }

  // 🔍 Debug: Log first item to console to see exact property names
  if (debug && documents.length > 0) {
    console.log('🔍 document API Response Shape:', documents[0])
  }

  const handleRemoveDocument = async (id) => {
    await removeDocument(id)
    queryCache.invalidateQueries(['folders', folderId, 'documents'])
    if (!folderId) queryCache.invalidateQueries('documents')
  }

  const parentUrl = parentId ? `/documents/${parentId}` : '/documents'
  const MAX_VISIBLE = 12
  const visibledocuments = documents.slice(0, MAX_VISIBLE)

  if (queryError) {
    return (
      <Container className="mt-4">
        <Alert variant="danger">
          <BsExclamationTriangle className="me-2" />
          {t('errorLoading', 'Failed to load data')}: {queryError.message}
        </Alert>
        <Button onClick={() => history.push('/documents')}>{t('backToRoot', 'Go to Root')}</Button>
      </Container>
    )
  }

  return (
    <Container fluid className="py-4">
      {/* Header */}
      <Row className="mb-4 align-items-center">
        <Col>
          <h2 className="mb-0">
            {isFolderLoading ? <DefaultSpinner /> : <><BsFolder className="me-2 text-primary" />{folderName}</>}
          </h2>
        </Col>
        <EditFolderButtons folderId={folderId} />
      </Row>

      {/* Debug Toggle */}
      <div className="mb-3 text-end">
        <Button size="sm" variant="outline-secondary" onClick={() => setDebug(!debug)}>
          {debug ? 'Hide Debug' : 'Show Debug'}
        </Button>
      </div>

      {/* Subfolders */}
      <h4 className="border-bottom pb-2 mb-3">
        {folderId && (
          <Button as={Link} to={parentUrl} size="sm" variant="outline-secondary" className="me-2">
            <BsArrowUp className="me-1" /> {t('back', 'Back')}
          </Button>
        )}
        {t('subfolders', 'Subfolders')}
      </h4>

      <Row className="mb-5">
        {isFolderLoading ? (
          <Col className="text-center"><DefaultSpinner /></Col>
        ) : folders.length > 0 ? (
          folders.map((folder) => (
            <Col key={folder.id} md={3} sm={4} className="mb-3">
              <Card className="bg-light h-100" style={{ borderLeft: '4px solid #226040' }}>
                <Card.Body>
                  <Card.Title>
                    <Link to={`/documents/${folder.id}`} className="text-decoration-none text-dark fw-bold">
                      <BsFolder className="me-2" /> {folder.name || folder.title || t('unnamed', 'Untitled')}
                    </Link>
                  </Card.Title>
                </Card.Body>
              </Card>
            </Col>
          ))
        ) : (
          <Col><p className="text-muted">{t('noSubfolders', 'No subfolders')}</p></Col>
        )}
      </Row>

      {/* Documents */}
      <h4 className="border-bottom pb-2 mb-3">{t('documents', 'Documents')}</h4>
      <Row>
        {isdocumentLoading ? (
          <Col className="text-center"><DefaultSpinner /></Col>
        ) : visibledocuments.length > 0 ? (
          visibledocuments.map((kron) => (
            <documentCard key={kron.id} document={kron} onRemove={handleRemoveDocument} t={t} />
          ))
        ) : (
          <Col><Alert variant="info">{t('noDocuments', 'No documents in this folder.')}</Alert></Col>
        )}
      </Row>

      {/* Actions */}
      <Row className="mt-4">
        <Col>
          <Can I='create' a='Folder'>
            <Button as={Link} to="/folders/new" variant="primary" className="me-2">
              <BsFolder className="me-2" /> {t('addFolder', 'New Folder')}
            </Button>
          </Can>
          <Can I='create' a='document'>
            <Button as={Link} to="/documents/new" variant="success">
              <BsFileText className="me-2" /> {t('addDocument', 'Upload Document')}
            </Button>
          </Can>
        </Col>
      </Row>
    </Container>
  )
}

export default documents