import React from 'react'
import { useParams } from 'react-router-dom'
import { useQuery } from 'react-query'
import { Container, Spinner } from 'react-bootstrap'
import { getDocumentById } from './queries'

const DocumentView = () => {
  const { id } = useParams()

  const { data, isLoading } = useQuery(
    ['document', id],
    () => getDocumentById(null, id)
  )

  if (isLoading) return <Spinner animation="border" />

  if (!data) return <div>Document not found</div>

  // IMPORTANT: backend must return real file URL
  const fileUrl =
    data.url ||
    data.file_url ||
    data.download_url

  if (!fileUrl) {
    return <div>No file URL provided by API</div>
  }

  return (
    <Container className="py-3">
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