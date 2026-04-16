import React from 'react'
import { useQueryCache } from 'react-query'
import { useHistory } from 'react-router-dom'
import NewObjectComponent from '../Generic/NewObjectComponent'
import { createCommittee } from './queries'
import CommitteeForm from './CommitteeForm'


const NewCommittee = () => {
  const queryCache = useQueryCache()
  const history = useHistory()

  const onSuccess = (savedCommittee) => {
    queryCache.setQueryData(
      ['committees', savedCommittee.id],
      savedCommittee
    )

    queryCache.invalidateQueries('committees')

    history.push('/committees')
  }

  return (
    <NewObjectComponent
      objectName='committee'
      createFunction={createCommittee}
      onSuccess={onSuccess}
      FormComponent={CommitteeForm}
    />
  )
}

export default NewCommittee