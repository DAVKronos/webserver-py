import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Alert, Button } from 'react-bootstrap'
import { BsArrowUpRight, BsCalendar3, BsClock, BsGeoAlt, BsPeople } from 'react-icons/bs'
import { format } from '../../utils/date-format'
import MonthSwitcher from '../Generic/MonthSwitcher'
import { useQuery } from 'react-query'
import { getAgendaitems } from './queries'
import { parseParams } from '../../utils/generic'
import DefaultSpinner from '../Generic/Spinner'
import { Can } from '../../utils/auth-helper'
import { useTranslation } from 'react-i18next'
import MultiLanguageText from '../Generic/MultiLanguageText'
import { AgendaItemTypeName } from './AgendaItemType'

const AgendaItems = () => {
  const { search } = useLocation()
  const { t, i18n } = useTranslation('generic')
  const lang = i18n.language
  const queryParams = parseParams(search)
  const date = queryParams.year && queryParams.month
    ? new Date(queryParams.year, queryParams.month - 1)
    : new Date()

  const {
    isLoading,
    isError,
    data: agendaItems = [],
    refetch
  } = useQuery(
    ['agendaitems', { year: date.getFullYear(), month: date.getMonth() }],
    getAgendaitems
  )

  return (
    <div className='agenda-page'>
      <header className='agenda-page-header'>
        <div className='agenda-page-heading'>
          <span className='agenda-page-eyebrow'>
            <BsCalendar3 aria-hidden='true' />
            {t('agendaItemPage:eyebrow')}
          </span>
          <h1>{t('agendaItemPage:header')}</h1>
          <p>{t('agendaItemPage:intro')}</p>
        </div>

        <Can I='create' a='AgendaItem'>
          <Button as={Link} to='/agendaitems/new' className='agenda-create-button'>
            {t('addModel', {
              model: t('models:modelNames.agendaItem', { count: 0 })
            })}
            <BsArrowUpRight aria-hidden='true' />
          </Button>
        </Can>
      </header>

      <section className='agenda-schedule' aria-label={t('agendaItemPage:monthSchedule')}>
        <div className='agenda-schedule-toolbar'>
          <div className='agenda-schedule-month'>
            <span className='agenda-schedule-icon'><BsCalendar3 aria-hidden='true' /></span>
            <div>
              <span className='agenda-schedule-label'>{t('agendaItemPage:monthSchedule')}</span>
              <h2>{format(date, 'MMMM yyyy', lang)}</h2>
            </div>
          </div>
          <MonthSwitcher date={date} />
        </div>

        {isLoading && (
          <div className='agenda-state agenda-loading'>
            <DefaultSpinner />
          </div>
        )}

        {isError && (
          <Alert variant='danger' className='agenda-error'>
            <div>
              <strong>{t('agendaItemPage:loadErrorTitle')}</strong>
              <div>{t('agendaItemPage:loadErrorDescription')}</div>
            </div>
            <Button variant='outline-danger' onClick={() => refetch()}>
              {t('agendaItemPage:retry')}
            </Button>
          </Alert>
        )}

        {!isLoading && !isError && agendaItems.length === 0 && (
          <div className='agenda-state agenda-empty'>
            <span className='agenda-empty-icon'><BsCalendar3 aria-hidden='true' /></span>
            <div>
              <h3>{t('agendaItemPage:noEventsTitle')}</h3>
              <p>{t('agendaItemPage:noEventsDescription')}</p>
            </div>
          </div>
        )}

        {!isLoading && !isError && agendaItems.length > 0 && (
          <div className='agenda-event-list'>
            {agendaItems.map(item => {
              const itemDate = new Date(item.date)
              return (
                <Link key={item.id} to={`/agendaitems/${item.id}`} className='agenda-event'>
                  <span className='agenda-event-date'>
                    <span className='agenda-event-weekday'>{format(itemDate, 'ccc', lang)}</span>
                    <span className='agenda-event-day'>{format(itemDate, 'd', lang)}</span>
                    <span className='agenda-event-month'>{format(itemDate, 'MMM', lang)}</span>
                  </span>
                  <span className='agenda-event-content'>
                    {item.agendaitem_type && (
                      <span className='agenda-event-type'>
                        <AgendaItemTypeName agendaItemType={item.agendaitem_type} />
                      </span>
                    )}
                    <span className='agenda-event-title'>
                      <MultiLanguageText nl={item.name_nl} en={item.name_en} />
                    </span>
                    {item.location && (
                      <span className='agenda-event-location'>
                        <BsGeoAlt aria-hidden='true' />
                        {item.location}
                      </span>
                    )}
                    {Array.isArray(item.subscriptions) && (
                      <span className='agenda-event-signups'>
                        <BsPeople aria-hidden='true' />
                        {t('agendaItemPage:subscriptions.count', { count: item.subscriptions.length })}
                      </span>
                    )}
                  </span>
                  <span className='agenda-event-time'>
                    <BsClock aria-hidden='true' />
                    {format(itemDate, 'p', lang)}
                  </span>
                  <BsArrowUpRight className='agenda-event-arrow' aria-hidden='true' />
                </Link>
              )
            })}
          </div>
        )}
      </section>
    </div>
  )
}

export default AgendaItems
