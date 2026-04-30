import React, { useState } from 'react'
import { Row, Col, Card, Container, Button } from 'react-bootstrap'
import { Link } from 'react-router-dom'
import { useQuery } from 'react-query'
import { BsFileText, BsFolder } from 'react-icons/bs'
import DefaultSpinner from '../Generic/Spinner'
import { getFolders, getDocuments } from './queries'

const DocumentExplorer = ({ folderId = null }) => {
  const [showAll, setShowAll] = useState(false)

  /* ---------------- SAFE FOLDER ID ---------------- */
  const safeFolderId =
    folderId && !Number.isNaN(Number(folderId))
      ? Number(folderId)
      : null

  /* ---------------- FOLDERS ---------------- */
  const { data: foldersData = [], isLoading: foldersLoading } = useQuery(
    ['folders'],
    () => getFolders()
  )

  /* ---------------- DOCUMENTS (ONLY INSIDE FOLDER) ---------------- */
  const { data: documents = [], isLoading: docsLoading } = useQuery(
    ['documents', safeFolderId],
    () => getDocuments(safeFolderId),
    {
      enabled: !!safeFolderId // only fetch inside folder
    }
  )

  /* ---------------- FILTER FOLDERS ---------------- */
  const folders = foldersData.filter(f => {
    const parentId = f.parent_folder_id ?? null

    return safeFolderId
      ? Number(parentId) === Number(safeFolderId)
      : parentId === null
  })

  const visibleDocs = safeFolderId
    ? (showAll ? documents : documents.slice(0, 8))
    : []

  /* ---------------- UI ---------------- */
  return (
    <Container fluid className="py-4">

      {/* ---------------- HEADER + ACTIONS ---------------- */}
      <div className="d-flex justify-content-between align-items-center mb-3">

        <h4 className="mb-0">
          <BsFolder className="me-2 text-warning" />
          Folders
        </h4>

        <div className="d-flex gap-2">

          {/* ADD FOLDER */}
          <Link to={safeFolderId ? `/folders/new?parent=${safeFolderId}` : `/folders/new`}>
            <Button size="sm" variant="outline-warning">
              + Folder
            </Button>
          </Link>

          {/* ADD DOCUMENT */}
          {safeFolderId && (
            <Link to={`/documents/new?folder=${safeFolderId}`}>
              <Button size="sm" variant="outline-primary">
                + Document
              </Button>
            </Link>
          )}

        </div>
      </div>

      {/* ---------------- FOLDERS ---------------- */}
      <Row className="mb-4">
        {foldersLoading ? (
          <Col><DefaultSpinner /></Col>
        ) : folders.length > 0 ? (
          folders.map(f => (
            <Col md={3} sm={4} key={f.id} className="mb-3">
              <Card className="bg-light shadow-sm">
                <Card.Body>
                  <Link to={`/folders/${f.id}`}>
                    <BsFolder className="me-2 text-warning" />
                    {f.name || f.title}
                  </Link>
                </Card.Body>
              </Card>
            </Col>
          ))
        ) : (
          <Col className="text-muted">No folders</Col>
        )}
      </Row>

      {/* ---------------- DOCUMENTS ---------------- */}
      {safeFolderId && (
        <>
          <hr />

          <h4 className="mb-3">
            <BsFileText className="me-2 text-primary" />
            Documents
          </h4>

          <Row>
            {docsLoading ? (
              <Col><DefaultSpinner /></Col>
            ) : visibleDocs.length > 0 ? (
              visibleDocs.map(doc => (
                <Col md={3} sm={4} key={doc.id} className="mb-3">
                  <Card className="shadow-sm">
                    <Card.Body>
                      <Link to={`/documents/${doc.id}`}>
                        <BsFileText className="me-2 text-primary" />
                        {doc.name || doc.file_name}
                      </Link>
                    </Card.Body>
                  </Card>
                </Col>
              ))
            ) : (
              <Col>No documents</Col>
            )}
          </Row>

          {/* LOAD ALL */}
          {!showAll && documents.length > 8 && (
            <div className="text-center mt-3">
              <Button variant="outline-primary" onClick={() => setShowAll(true)}>
                Show all
              </Button>
            </div>
          )}
        </>
      )}


    </Container>
  )
}

export default DocumentExplorer