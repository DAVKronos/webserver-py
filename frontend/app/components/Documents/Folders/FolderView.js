import React from 'react'
import { useParams } from 'react-router-dom'
import DocumentExplorer from '../DocumentExplorer'

const FolderView = () => {
  const { id } = useParams()

  return <DocumentExplorer folderId={parseInt(id)} />
}

export default FolderView