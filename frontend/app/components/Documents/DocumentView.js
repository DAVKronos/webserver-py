import React from 'react'
import { useParams } from 'react-router-dom'
import { useQuery } from 'react-query'
import { getDocumentById } from './queries'
import { Container, Spinner } from 'react-bootstrap'

const DocumentView = () => {
  const { id } = useParams()

  const { data, isLoading, error } = useQuery(
    ['document', id],
    () => getDocumentById(null, id)
  )

  if (isLoading) return <Spinner animation="border" />
  if (error) return <div>Error loading document</div>

  // 🔥 IMPORTANT: backend likely serves file via endpoint
  const fileUrl =
    data.display_url ||
    data.download_url ||
    `/api/v1/documents/${id}/display/original`

  return (
    <Container fluid className="py-3">

      <h4>{data.file_name}</h4>

      <iframe
        src={fileUrl}
        width="100%"
        height="800px"
        title={data.file_name}
      />

    </Container>
  )
}

export default DocumentView