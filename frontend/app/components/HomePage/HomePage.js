import React from 'react'
import NewsItems from './HomePageNewsItems'
import AgendaItemsSidebar from './AgendaItemsSidebar'
import UserBirthdays from './UserBirthdays'
import { useTranslation } from 'react-i18next'
import { Can } from '../../utils/auth-helper'
import Announcement from './Announcement'
import { Link } from 'react-router-dom'


const HomePage = () => {
  const { t } = useTranslation('homepage')
  const { t: tNavigation } = useTranslation('navigation')
  return (
    <div className='home-page'>
      <div className='home-announcement-row'>
        <Announcement />
      </div>
      <section className='home-section-heading'>
        <div>
          <span className='home-kicker'>DAV KRONOS <span aria-hidden='true'>/</span> ENSCHEDE</span>
          <h1>{t('news')}</h1>
        </div>
        <Link className='home-agenda-link' to='/agendaitems'>
          {tNavigation('agenda')}
          <span aria-hidden='true'>↗</span>
        </Link>
      </section>
      <div className='home-content-row'>
        <section className='home-news-column' aria-label={t('news')}>
          <NewsItems />
        </section>
        <aside className='home-sidebar'>
          <AgendaItemsSidebar />
          <Can I='view' a='User'>
            <UserBirthdays />
          </Can>
        </aside>
      </div>
    </div>
  )
}

export default HomePage
