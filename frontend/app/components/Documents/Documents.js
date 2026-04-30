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

/* ================= DOCUMENT CARD ================= */

const DocumentCard = ({ document, onRemove, t }) => {
  const title =
    document.name ||
    document.title ||
    document.file_name ||
    t('untitled', 'Untitled')

  return (
    <Col md={3} sm={4} className="mb-4">
      <Card className="h-100 shadow-sm">
        <Card.Body className="d-flex flex-column">

          {/* ALWAYS FILE VIEW */}
          <Card.Title className="h6">
            <Link
              to={`/documents/${document.id}`}
              className="text-dark text-decoration-none"
            >
              <BsFileText className="me-2 text-primary" />
              {title}
            </Link>
          </Card.Title>

          <div className="mt-auto d-flex gap-2">
            <Can I="delete" a="document">
              <Button
                size="sm"
                variant="danger"
                onClick={() => onRemove(document.id)}
              >
                {t('delete', 'Delete')}
              </Button>
            </Can>
          </div>

        </Card.Body>
      </Card>
    </Col>
  )
}

/* ================= FOLDER CARD ================= */

const FolderCard = ({ folder }) => {
  return (
    <Col md={3} sm={4} className="mb-4">
      <Card className="bg-light shadow-sm">
        <Card.Body>
          <Link
            to={`/folders/${folder.id}`}
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

/* ================= MAIN PAGE ================= */

const Documents = () => {
  const { t } = useTranslation('documentPage')
  const queryCache = useQueryCache()
  const [showAll, setShowAll] = useState(false)

  /* ---------- DATA ---------- */

  const {
    data: documents = [],
    isLoading: docsLoading,
    error: docsError
  } = useQuery('documents', getDocuments)

  const {
    data: folders = [],
    isLoading: foldersLoading,
    error: foldersError
  } = useQuery('folders', getFolders)

  /* ---------- DELETE ---------- */

  const handleRemoveDocument = async (id) => {
    await removeDocument(id)
    queryCache.invalidateQueries('documents')
  }

  /* ---------- FILTER TOP FOLDERS ONLY ---------- */
  const topFolders = folders.filter(
    f => !f.parent_folder_id || f.parent_folder_id === 0
  )

  const visibleDocuments = showAll
    ? documents
    : documents.slice(0, 8)

  /* ---------- ERROR ---------- */

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

  return (
    <Container fluid className="py-4">

      {/* HEADER */}
      <h2 className="mb-4">
        Documents & Folders
      </h2>

      {/* ================= FOLDERS ================= */}
      <h4 className="mb-3">
        <BsFolder className="me-2 text-warning" />
        Folders
      </h4>

      <Row className="mb-4">
        {foldersLoading ? (
          <Col><DefaultSpinner /></Col>
        ) : topFolders.length > 0 ? (
          topFolders.map(folder => (
            <FolderCard key={folder.id} folder={folder} />
          ))
        ) : (
          <Col className="text-muted">
            No folders
          </Col>
        )}
      </Row>

      <hr />

      {/* ================= DOCUMENTS ================= */}
      <h4 className="mb-3">
        <BsFileText className="me-2 text-primary" />
        Documents
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
          <Col className="text-muted">
            No documents
          </Col>
        )}
      </Row>

      {/* LOAD ALL */}
      {!showAll && documents.length > 8 && (
        <div className="text-center mt-3">
          <Button
            variant="outline-primary"
            onClick={() => setShowAll(true)}
          >
            Load all
          </Button>
        </div>
      )}

      {/* UPLOAD */}
      <Row className="mt-4">
        <Col>
          <Can I="create" a="document">
            <Button as={Link} to="/documents/new" variant="success">
              Upload Document
            </Button>
          </Can>
        </Col>
      </Row>

    </Container>
  )
}

export default Documents