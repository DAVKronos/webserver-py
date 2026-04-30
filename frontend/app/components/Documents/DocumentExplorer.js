import React, { useState } from 'react'
import { Row, Col, Card, Container, Button } from 'react-bootstrap'
import { Link } from 'react-router-dom'
import { useQuery } from 'react-query'
import { BsFileText, BsFolder } from 'react-icons/bs'
import DefaultSpinner from '../Generic/Spinner'
import { getFolders, getDocuments } from './queries'

const DocumentExplorer = ({ folderId = null }) => {
  const [showAll, setShowAll] = useState(false)

  /* ---------------- FOLDERS ---------------- */
  const { data: foldersData = [], isLoading: foldersLoading } = useQuery(
    ['folders'],
    () => getFolders()
  )

  /* ---------------- DOCUMENTS (ONLY INSIDE FOLDER) ---------------- */
  const { data: documents = [], isLoading: docsLoading } = useQuery(
    ['documents', folderId],
    () => getDocuments(folderId),
    {
      enabled: !!folderId   // 🚨 IMPORTANT: only load inside folder
    }
  )

  /* ---------------- FILTER FOLDERS ---------------- */
  const folders = foldersData.filter(f => {
    const parentId = f.parent_folder_id ?? null

    return folderId
      ? Number(parentId) === Number(folderId)
      : parentId === null
  })

  const visibleDocs = folderId
    ? (showAll ? documents : documents.slice(0, 8))
    : []

  return (
    <Container fluid className="py-4">

      {/* ---------------- FOLDERS ---------------- */}
      <h4>
        <BsFolder className="me-2 text-warning" />
        Folders
      </h4>

      <Row className="mb-4">
        {foldersLoading ? (
          <Col><DefaultSpinner /></Col>
        ) : folders.length ? (
          folders.map(f => (
            <Col md={3} key={f.id}>
              <Card>
                <Card.Body>
                  <Link to={`/folders/${f.id}`}>
                    <BsFolder className="me-2 text-warning" />
                    {f.name}
                  </Link>
                </Card.Body>
              </Card>
            </Col>
          ))
        ) : (
          <Col>No folders</Col>
        )}
      </Row>

      <hr />

      {/* ---------------- DOCUMENTS ---------------- */}
      {folderId && (
        <>
          <h4>
            <BsFileText className="me-2 text-primary" />
            Documents
          </h4>

          <Row>
            {docsLoading ? (
              <Col><DefaultSpinner /></Col>
            ) : visibleDocs.length ? (
              visibleDocs.map(doc => (
                <Col md={3} key={doc.id}>
                  <Card>
                    <Card.Body>
                      <Link to={`/documents/${doc.id}`}>
                        <BsFileText className="me-2" />
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
              <Button onClick={() => setShowAll(true)}>
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