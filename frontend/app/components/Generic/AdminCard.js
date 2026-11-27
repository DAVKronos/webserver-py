import React from 'react'
import { Card } from 'react-bootstrap'
import { useTranslation } from 'react-i18next'

// "Settings" card with admin buttons, for the side column of a page.
// Give the buttons the `block` prop: full width, above each other (Bootstrap's btn-block spacing).
const AdminCard = ({ children }) => {
  const { t } = useTranslation('generic')
  return (
    <Card className='mt-5'>
      <Card.Header><h6 className='mb-0'>{t('settings')}</h6></Card.Header>
      <Card.Body>{children}</Card.Body>
    </Card>
  )
}

export default AdminCard
