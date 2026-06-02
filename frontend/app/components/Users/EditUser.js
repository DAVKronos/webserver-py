import React from 'react'
import { useQuery, useQueryCache } from 'react-query'
import DefaultSpinner from '../Generic/Spinner'
import { useHistory } from 'react-router-dom'
import EditObjectComponent from '../Generic/EditObjectComponent'
import { getUser, updateUser } from './queries'
import { ability } from '../../utils/auth-helper'
import { subject } from '@casl/ability'
import UserForm, { adminEditUserFields, limitedEditUserFields } from './UserForm'

const EditUserWithData = (props) => {
  const id = parseInt(props.match.params.id)
  const { isLoading, isError, data, error } = useQuery(['users', id], getUser)
  if (isLoading) {
    return <DefaultSpinner />
  }
  return data && <EditUser user={data} />
}

const EditUser = ({ user }) => {
  const queryCache = useQueryCache()
  const history = useHistory()
  const { id, name } = user
  const editableFields = Object.fromEntries(
    adminEditUserFields
      .filter((fieldObject) => fieldObject.type != 'file')
      .map((fieldObject) => [fieldObject.name, user[fieldObject.name] ?? ''])
  )

  const onSuccess = (savedUser) => {
    queryCache.setQueryData(['users', savedUser.id], savedUser)
    history.push(`/users/${savedUser.id}`)
  }

  const admin = ability.can('edit.extended', subject('User', user))
  const fields = admin ? adminEditUserField : limitedEditUserField
  
  return (
    <EditObjectComponent
      id={id}
      existingObject={editableFields}
      objectName='user'
      updateFunction={updateUser}
      onSuccess={onSuccess}
      FormComponent={UserForm}
      fields={fields}
    />
  )
}

export default EditUserWithData
