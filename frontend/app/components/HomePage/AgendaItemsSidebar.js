import React from 'react'
import AgendaItem from './AgendaItem'
import { Card, ListGroup } from 'react-bootstrap'
import { useQuery } from 'react-query'
import { useTranslation } from 'react-i18next'
import { getAgendaitems } from '../AgendaItems/queries'
import DefaultSpinner from '../Generic/Spinner'

function AgendaItemsSideBar () {
  const { t } = useTranslation('homepage')
  const { isLoading, isError, data } = useQuery('agendaitems', agendaItems)
  const agendaitems = (data || [])
    .filter(agendaitem => {
      const typeName = agendaitem.agendaitem_type?.name_nl || ''
      return !typeName.toLowerCase().includes('training')
    })
    .slice(0, 3)
  let content
  if (isLoading) {
    content = <DefaultSpinner />
  } else if (isError) {
    content = <p className='agenda-sidebar-empty'>{t('agendaLoadError')}</p>
  } else if (!agendaitems.length) {
    content = <p className='agenda-sidebar-empty'>{t('noUpcomingAgenda')}</p>
  } else {
    content = agendaitems.map((item, index) => (
      <ListGroup.Item
        key={item.id}
        className={index === 0 ? 'agenda-sidebar-item agenda-sidebar-item-featured' : 'agenda-sidebar-item'}
      >
        <AgendaItem item={item} />
      </ListGroup.Item>
    ))
  }

  return (
    <Card className='side-panel agenda-sidebar'>
      <Card.Header>Agenda</Card.Header>
      <ListGroup variant='flush'>
        {content}
      </ListGroup>
    </Card>
  )
}

function sortAgendaItems (a, b) {
  return new Date(a.date) - new Date(b.date)
}

function agendaItems (queryKey) {
  const now = new Date()
  const nextMonth = new Date(now.getFullYear(), now.getMonth() + 1)
  const params = { year: nextMonth.getFullYear(), month: nextMonth.getMonth() }
  return Promise.all([getAgendaitems(queryKey), getAgendaitems(queryKey, params)])
    .then(([agendaItems1, agendaItems2]) => {
      return agendaItems1.concat(agendaItems2).filter(agendaItem => {
        const agendaDate = new Date(agendaItem.date)
        return agendaDate >= now
      }).sort(sortAgendaItems)
    })
}

export default AgendaItemsSideBar
