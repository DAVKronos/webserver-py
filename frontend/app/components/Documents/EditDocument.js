import React from 'react'
import { useQuery, useQueryCache } from 'react-query'
import DefaultSpinner from '../Generic/Spinner'
import { useHistory } from 'react-router-dom'
import EditObjectComponent from '../Generic/EditObjectComponent'
import { getDocumentById, updateDocument } from './queries'
import documentForm from './DocumentForm'

const EditdocumentWithData = (props) => {
  const id = parseInt(props.match.params.id)
  const { isLoading, isError, data, error } = useQuery(['documents', id], getDocumentById)
  if (isLoading) {
    return <DefaultSpinner />
  }
  return data && <Editdocument document={data} />
}

const Editdocument = ({ document }) => {
  const queryCache = useQueryCache()
  const history = useHistory()
  const { id, name, folder_id, date } = document
  const isPublic = document.public
  const editableFields = { name, folder_id, date, public: isPublic }
  const onSuccess = (saveddocument) => {
    queryCache.setQueryData(['documents', saveddocument.id], saveddocument)
    if (saveddocument.folder_id) {
      history.push(`/documents/${saveddocument.folder_id}`)
    } else {
      history.push('/documents')
    }
  }

  return (
    <EditObjectComponent
      id={id}
      existingObject={editableFields}
      objectName='document'
      updateFunction={updateDocument}
      onSuccess={onSuccess}
      FormComponent={documentForm}
    />
  )
}

export default EditdocumentWithData
