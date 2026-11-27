import React from 'react'
import { useQuery, useQueryCache } from 'react-query'
import { Button, Table } from 'react-bootstrap'
import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { deleteAgendaItemType, getAgendaItemTypes } from './queries'
import { Can } from '../../utils/auth-helper'
import RemoveButton from '../Generic/RemoveButton'

const AgendaItemTypes = () => {
  const { t } = useTranslation('generic')
  const queryCache = useQueryCache()
  const { isLoading, isError, data: agendaItemTypes, error } = useQuery('agendaItemTypes', getAgendaItemTypes)

  const onClickRemove = (id) => {
    deleteAgendaItemType(id).then(() => {
      queryCache.invalidateQueries('agendaItemTypes')
    })
  }

  return (
    <>
      <h1>Agendaitem types</h1>
      <Table>
        <thead>
          <tr>
            <th colSpan={3}>
              Naam
            </th>
          </tr>
        </thead>
        <tbody>
          {agendaItemTypes && agendaItemTypes.map(({ id, name }) => {
            return (
              <tr key={id}>
                <td>{name}</td>
                <td>
                  <Can I='update' an='Agendaitemtype'>
                    <Button variant='warning' as={Link} to={`/agendaitemtypes/${id}/edit`}>{t('edit')}</Button>
                  </Can>
                </td>
                <td>
                  <Can I='destroy' an='Agendaitemtype'>
                    <RemoveButton variant='danger' onRemove={() => onClickRemove(id)}>{t('remove')}</RemoveButton>
                  </Can>
                </td>
              </tr>
            )
          })}
        </tbody>
      </Table>
      <Can I='create' an='Agendaitemtype'>
        <Button as={Link} to='/agendaitemtypes/new'>{t('add')}</Button>
      </Can>
    </>
  )
}

export default AgendaItemTypes
