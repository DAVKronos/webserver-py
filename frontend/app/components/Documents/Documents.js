import React, { useState } from 'react'
import { Row, Col, Card, Button, Container, Alert } from 'react-bootstrap'
import { Link } from 'react-router-dom'
import { useQuery, useQueryCache } from 'react-query'
import { useTranslation } from 'react-i18next'

import {
  getDocuments,
  getFolders,
  removeDocument
} from './queries'

import DefaultSpinner from '../Generic/Spinner'
import { BsFileText, BsFolder, BsExclamationTriangle } from 'react-icons/bs'
import { Can } from '../../utils/auth-helper'

/* ---------------- DOCUMENT CARD ---------------- */

const DocumentCard = ({ document, onRemove, t }) => {
  const title =
    document.name ||
    document.title ||
    document.file_name ||
    t('untitled', 'Untitled')

  const handleRemove = async () => {
    if (!window.confirm(t('confirmDeleteDoc', 'Delete document?'))) return
    await onRemove(document.id)
  }

  return (
    <Col md={3} sm={4} className="mb-4">
      <Card className="h-100 shadow-sm">
        <Card.Body className="d-flex flex-column">
          <Card.Title className="h6">
            <Link
              to={`/documents/${document.id}`}   // ✅ ALWAYS file → document view
              className="text-dark text-decoration-none"
            >
              <BsFileText className="me-2 text-primary" />
              {title}
            </Link>
          </Card.Title>

          <div className="mt-auto d-flex gap-2">
            <Can I='delete' a='document'>
              <Button size="sm" variant="danger" onClick={handleRemove}>
                {t('delete', 'Delete')}
              </Button>
            </Can>
          </div>
        </Card.Body>
      </Card>
    </Col>
  )
}

/* ---------------- FOLDER CARD ---------------- */

const FolderCard = ({ folder }) => {
  return (
    <Col md={3} sm={4} className="mb-4">
      <Card className="bg-light shadow-sm">
        <Card.Body>
          <Link
            to={`/folders/${folder.id}`}   // ✅ folders go to folders route
            className="text-dark text-decoration-none"
          >
            <BsFolder className="me-2 text-warning" />
            {folder.name || folder.title}
          </Link>
        </Card.Body>
      </Card>
    </Col>
  )
}

/* ---------------- MAIN PAGE ---------------- */

const Documents = () => {
  const { t } = useTranslation('documentPage')
  const queryCache = useQueryCache()
  const [showAll, setShowAll] = useState(false)

  const {
    data: documents = [],
    isLoading: docsLoading,
    error: docsError
  } = useQuery('documents', getDocuments)

  const {
  data: foldersData = [],
  isLoading: foldersLoading,
  error: foldersError
  } = useQuery('folders', getFolders)

  const folders = foldersData.filter(
    f => f.parent_folder_id === null || f.parent_folder_id === 0
    )


  const handleRemoveDocument = async (id) => {
    await removeDocument(id)
    queryCache.invalidateQueries('documents')
  }

  if (docsError || foldersError) {
    return (
      <Container className="mt-4">
        <Alert variant="danger">
          <BsExclamationTriangle className="me-2" />
          {t('errorLoading', 'Failed to load')}
        </Alert>
      </Container>
    )
  }

  const visibleDocuments = showAll ? documents : documents.slice(0, 8)

  return (
    <Container fluid className="py-4">

      {/* HEADER */}
      <h2 className="mb-4">
        {t('documentsAndFolders', 'Documents & Folders')}
      </h2>

      {/* ---------------- FOLDERS ---------------- */}
      <h4 className="mb-3">
        <BsFolder className="me-2 text-warning" />
        {t('folders', 'Folders')}
      </h4>

      <Row className="mb-4">
        {foldersLoading ? (
          <Col><DefaultSpinner /></Col>
        ) : folders.length > 0 ? (
          folders.map(folder => (
            <FolderCard key={folder.id} folder={folder} />
          ))
        ) : (
          <Col>
            <Alert variant="info">No folders</Alert>
          </Col>
        )}
      </Row>

      <hr />

      {/* ---------------- DOCUMENTS ---------------- */}
      <h4 className="mb-3">
        <BsFileText className="me-2 text-primary" />
        {t('documents', 'Documents')}
      </h4>

      <Row>
        {docsLoading ? (
          <Col><DefaultSpinner /></Col>
        ) : visibleDocuments.length > 0 ? (
          visibleDocuments.map(doc => (
            <DocumentCard
              key={doc.id}
              document={doc}
              onRemove={handleRemoveDocument}
              t={t}
            />
          ))
        ) : (
          <Col>
            <Alert variant="info">
              {t('noDocuments', 'No documents found')}
            </Alert>
          </Col>
        )}
      </Row>

      {/* LOAD ALL BUTTON */}
      {!showAll && documents.length > 8 && (
        <div className="text-center mt-3">
          <Button variant="outline-primary" onClick={() => setShowAll(true)}>
            {t('loadAll', 'Show all')}
          </Button>
        </div>
      )}

      {/* ACTION */}
      <Row className="mt-4">
        <Col>
          <Can I='create' a='document'>
            <Button as={Link} to="/documents/new" variant="success">
              {t('uploadDocument', 'Upload Document')}
            </Button>
          </Can>
        </Col>
      </Row>

    </Container>
  )
}

export default Documents