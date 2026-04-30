import React from 'react'
import { useParams, Link } from 'react-router-dom'
import { useQuery } from 'react-query'
import {  getFolderById,  getFolderDocuments} from '../queries'
import { Row, Col, Container } from 'react-bootstrap'

const FolderView = () => {
  const { id } = useParams()

  const { data: folder } = useQuery(['folder', id], () =>
    getFolderById(null, id)
  )

  const { data: docs = [] } = useQuery(['folderDocs', id], () =>
    getFolderDocuments(null, id)
  )

  return (
    <Container className="py-3">

      <h3>📁 {folder?.name}</h3>

      <Row>
        {docs.map(doc => (
          <Col key={doc.id}>
            <Link to={`/documents/${doc.id}`}>
              📄 {doc.file_name}
            </Link>
          </Col>
        ))}
      </Row>

    </Container>
  )
}

export default FolderView