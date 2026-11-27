import React from 'react'
import { ListGroup, Row, Col } from 'react-bootstrap'
import { NavLink } from 'react-router-dom'
import { useTranslation } from 'react-i18next'

const AdminHome = () => {
  const { t } = useTranslation('generic')
  return (
    <Row>
      <Col md={{ span: 8, offset: 2 }}>
        <h1>{t('adminPage')}</h1>
        <ListGroup>
          <ListGroup.Item as={NavLink} to='/admin/approve-news' action>Nieuwsitems goedkeuren</ListGroup.Item>
          {/* <ListGroup.Item as={NavLink} to='/admin/mailinglists' action>Mailinglijsten</ListGroup.Item>
          <ListGroup.Item as={NavLink} to='/admin/aliases' action>Aliassen</ListGroup.Item> */}
          <ListGroup.Item as={NavLink} to='/admin/pages' action>Informatie pagina&apos;s</ListGroup.Item>
          <ListGroup.Item as={NavLink} to='/admin/announcements' action>Banners</ListGroup.Item>
        </ListGroup>
      </Col>
    </Row>
  )
}

export default AdminHome
