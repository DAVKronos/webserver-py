import React, { useState } from 'react'
import { Table, Button } from 'react-bootstrap'
import { useQuery, useQueryCache } from 'react-query'
import { useTranslation } from 'react-i18next'
import {
  createCommitteeMembership,
  getCommittee,
  getCommitteeMemberships,
  removeCommitteeMembership
} from './queries'
import DefaultSpinner from '../Generic/Spinner'
import MultiLanguageText from '../Generic/MultiLanguageText'
import { FieldControl } from '../Generic/FormField'
import { Can } from '../../utils/auth-helper'

import { getUsers } from '../Users/queries'


const NewCommitteeMember = ({ CommitteeId }) => {
  const [userId, setUserId] = useState(null)
  const [CommitteeFunction, setCommitteeFunction] = useState(null)
  const [creating, setCreating] = useState(false)
  const { t } = useTranslation('generic')
  const queryCache = useQueryCache()

  const onClickCreate = () => {
    if (userId && CommitteeFunction) {
      setCreating(true)

      const data = {
        user_id: userId,
        function: CommitteeFunction,
        committee_id: CommitteeId
      }

      createCommitteeMembership(CommitteeId, data).then(() => {
        setCreating(false)
        queryCache.invalidateQueries(
          ['committees', CommitteeId, 'committee_memberships'],
          { exact: true }
        )
        setUserId(null)
        setCommitteeFunction(null)
      })
    }
  }

  return (
    <tr>
      <td>
        <FieldControl
          value={userId}
          setValue={(v) => setUserId(v)}
          type='reference'
          required
          size='sm'
          itemQuery={[['users'], getUsers]}
        />
      </td>
      <td>
        <FieldControl
          value={CommitteeFunction}
          setValue={(v) => setCommitteeFunction(v)}
          type='text'
          required
        />
      </td>
      <td>
        <Button onClick={onClickCreate} size='sm' variant='success'>
          {creating ? <DefaultSpinner inline size='sm' /> : t('add')}
        </Button>
      </td>
    </tr>
  )
}


const CommitteeMembershipRow = ({ membership, removeFunction }) => {
  const name = membership.user && membership.user.name
  const [removing, setRemoving] = useState(false)

  const onClickRemove = () => {
    setRemoving(true)
    removeFunction(membership.id).then(() => {
      setRemoving(false)
    })
  }

  return (
    <tr key={membership.id}>
      <td>{name}</td>
      <td>{membership.function}</td>
      <td>
        <Can I='delete' a='CommitteeMembership'>
          <Button
            variant='danger'
            disabled={removing}
            size='sm'
            onClick={onClickRemove}
          >
            {removing ? <DefaultSpinner inline size='sm' /> : 'Verwijder'}
          </Button>
        </Can>
      </td>
    </tr>
  )
}


function Committee (props) {
  const id = parseInt(props.match.params.id)
  const queryCache = useQueryCache()

  const { isLoading, data } = useQuery(
    ['committees', id],
    getCommittee
  )

  const { isLoading: isMembershipsLoading, data: memberships } = useQuery(
    ['committees', id, 'committee_memberships'],
    getCommitteeMemberships
  )

  if (isLoading) {
    return <DefaultSpinner />
  }

  const Committee = data

  if (!Committee) {
    return <h1>Committee not found</h1>
  }

  const removeFunction = (membershipId) => {
    return removeCommitteeMembership(Committee.id, membershipId).then(() => {
      queryCache.invalidateQueries(
        ['committees', Committee.id, 'committee_memberships'],
        { exact: true }
      )
    })
  }

  return (
    <>
      <h1>
        <MultiLanguageText nl={Committee.name_nl} en={Committee.name_en} />
      </h1>

      <p className='lead'>
        <MultiLanguageText
          nl={Committee.description_nl}
          en={Committee.description_en}
        />
      </p>

      <Table striped>
        <thead>
          <tr>
            <th>Naam</th>
            <th>Functie</th>
            <Can I='delete' a='CommitteeMembership'>
              <th>Action</th>
            </Can>
          </tr>
        </thead>

        <tbody>
          {memberships &&
            memberships.map((membership) => {
              return (
                <CommitteeMembershipRow
                  key={membership.id}
                  removeFunction={removeFunction}
                  membership={membership}
                />
              )
            })}

          <Can I='create' a='CommitteeMembership'>
            <NewCommitteeMember CommitteeId={Committee.id} />
          </Can>
        </tbody>
      </Table>

      {isMembershipsLoading && <DefaultSpinner />}
    </>
  )
}

export default Committee