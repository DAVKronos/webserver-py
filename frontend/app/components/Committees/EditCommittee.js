import React from 'react'
import { useQuery, useQueryCache } from 'react-query'
import DefaultSpinner from '../Generic/Spinner'
import { useHistory } from 'react-router-dom'
import EditObjectComponent from '../Generic/EditObjectComponent'
import { getCommittee, updateCommittee } from './queries'
import CommitteeForm from './CommitteeForm'


const EditCommitteeWithData = (props) => {
  const id = parseInt(props.match.params.id)

  const { isLoading, data } = useQuery(
    ['committees', id],
    getCommittee
  )

  if (isLoading) {
    return <DefaultSpinner />
  }

  return data && <EditCommittee committee={data} />
}


const EditCommittee = ({ committee }) => {
  const queryCache = useQueryCache()
  const history = useHistory()

  const {
    id,
    name_nl,
    name_en,
    description_nl,
    description_en
  } = committee

  const editableFields = {
    name_nl,
    name_en,
    description_nl,
    description_en
  }

  const onSuccess = (savedCommittee) => {
    queryCache.setQueryData(
      ['committees', savedCommittee.id],
      savedCommittee
    )

    history.push(`/committees/${savedCommittee.id}`)
  }

  return (
    <EditObjectComponent
      id={id}
      existingObject={editableFields}
      objectName='committee'
      updateFunction={updateCommittee}
      onSuccess={onSuccess}
      FormComponent={CommitteeForm}
    />
  )
}

export default EditCommitteeWithData