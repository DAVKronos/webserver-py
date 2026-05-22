import React from 'react'
import { useQueryCache } from 'react-query'
import { useHistory } from 'react-router-dom'
import NewObjectComponent from '../Generic/NewObjectComponent'
import { createDocument } from './queries'
import documentForm from './DocumentForm'

const NewDocument = () => {
  const queryCache = useQueryCache()
  const history = useHistory()

  const onSuccess = (saveddocument) => {
    queryCache.setQueryData(['documents', saveddocument.id], saveddocument)
    queryCache.invalidateQueries('documents')
    if (saveddocument.folder_id) {
      history.push(`/documents/${saveddocument.folder_id}`)
    } else {
      history.push('/documents')
    }
  }

  return (
    <NewObjectComponent
      objectName='document'
      createFunction={createDocument}
      onSuccess={onSuccess}
      FormComponent={documentForm}
    />
  )
}

export default NewDocument
