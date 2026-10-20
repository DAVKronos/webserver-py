import React from 'react'
import { Row, Col } from 'react-bootstrap'
import NewsItems from './HomePageNewsItems'
import AgendaItemsSidebar from './AgendaItemsSidebar'
import StravaSidebar from './StravaSidebar'
import UserBirthdays from './UserBirthdays'
import { useTranslation } from 'react-i18next'
import { Can } from '../../utils/auth-helper'
import Announcement from './Announcement'


const HomePage = () => {
  const { t } = useTranslation('homepage')
  return (
    <>
      <Row className='home-announcement-row'>
        <Col md={12}>
          <Announcement />
        </Col>
      </Row>
      <Row className='home-section-heading'>
        <Col><h1>{t('news')}</h1></Col>
      </Row>
      <Row className='home-content-row'>
        <Col md={8}>
          <NewsItems />
        </Col>
        <Col md={4}>
          <AgendaItemsSidebar />
          {/* <StravaSidebar /> */}
          <Can I='view' a='User'>
            <UserBirthdays />
          </Can>
        </Col>
      </Row>
    </>
  )
}

export default HomePage
