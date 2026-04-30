import React from 'react'
import { useParams } from 'react-router-dom'
import DocumentExplorer from '../DocumentExplorer'

const FolderView = () => {
  const { id } = useParams()

  const folderId = id ? Number(id) : null

  // 🚨 prevent NaN
  const safeFolderId = Number.isNaN(folderId) ? null : folderId

  return <DocumentExplorer folderId={safeFolderId} />
}

export default FolderView