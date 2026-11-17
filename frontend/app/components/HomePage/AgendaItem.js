import React from 'react'
import { Row, Col } from 'react-bootstrap'
import { Link } from 'react-router-dom'
import { format } from '../../utils/date-format'
import { useTranslation } from 'react-i18next'
import { BsPersonFill } from 'react-icons/bs'
import MultiLanguageText from '../Generic/MultiLanguageText'

const AgendaItem = ({ item }) => {
  const date = new Date(item.date)
  const { i18n } = useTranslation('homepage')
  return (
    <Row as={Link} to={`/agendaitems/${item.id}`} className='agenda-sidebar-link'>
      <Col xs={3} className='agenda-sidebar-date'>
        <span className='agenda-sidebar-weekday'>{format(date, 'ccc', i18n.language)}</span>
        <span className='agenda-sidebar-day'>{date.getDate()}</span>
        <span className='agenda-sidebar-month'>{format(date, 'MMM', i18n.language)}</span>
      </Col>
      <Col xs={9} className='agenda-sidebar-title'>
        <h5><MultiLanguageText nl={item.name_nl} en={item.name_en} /></h5>
        {item.subscriptions?.length
          ? <span className='agenda-sidebar-subscriptions'><BsPersonFill aria-hidden='true' /> {item.subscriptions.length}</span>
          : null}
      </Col>
    </Row>
  )
  
} 

export default AgendaItem
