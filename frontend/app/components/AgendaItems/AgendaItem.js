import React from 'react'
import ReactMarkdown from 'react-markdown'
import { Alert, Button } from 'react-bootstrap'
import {
  BsArrowLeft,
  BsCalendar3,
  BsClock,
  BsGeoAlt,
  BsLink45Deg,
  BsPencil,
  BsTag,
  BsTrash
} from 'react-icons/bs'
import { format } from '../../utils/date-format'
import { useQuery } from 'react-query'
import { getAgendaitem, removeAgendaitem } from './queries'
import DefaultSpinner from '../Generic/Spinner'
import MultiLanguageText from '../Generic/MultiLanguageText'
import { Can } from '../../utils/auth-helper'
import { Link, useHistory } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { subject } from '@casl/ability'
import SubscriptionsCard from './Components/SubscriptionsCard'

function AgendaItem (props) {
  const { t, i18n } = useTranslation('agendaItemPage')
  const { t: tGeneric } = useTranslation('generic')
  const lang = i18n.language
  const history = useHistory()
  const id = parseInt(props.match.params.id)
  const { isLoading, isError, data: agendaItem, error, refetch } = useQuery(['agendaitems', id], getAgendaitem)

  if (isLoading) {
    return <DefaultSpinner />
  }

  if (isError) {
    if (error && error.response && error.response.status === 404) {
      return (
        <div className='agenda-detail-state'>
          <Alert variant='warning'>{t('detailNotFound')}</Alert>
        </div>
      )
    }

    return (
      <div className='agenda-detail-state'>
        <Alert variant='danger'>
          <strong>{t('detailLoadErrorTitle')}</strong>
          <div>{t('loadErrorDescription')}</div>
          <Button className='mt-3' variant='outline-danger' onClick={() => refetch()}>
            {t('retry')}
          </Button>
        </Alert>
      </div>
    )
  }

  if (!agendaItem) {
    return (
      <div className='agenda-detail-state'>
        <Alert variant='warning'>{t('detailNotFound')}</Alert>
      </div>
    )
  }

  const onClickRemove = () => {
    removeAgendaitem(id).then(() => {
      history.push('/agendaitems')
    })
  }

  const date = new Date(agendaItem.date)
  const eventUrl = agendaItem.url
    ? (/^https?:\/\//i.test(agendaItem.url) ? agendaItem.url : `http://${agendaItem.url}`)
    : null

  const renderDescription = (text) => <ReactMarkdown>{text}</ReactMarkdown>

  return (
    <article className='agenda-detail'>
      <header className='agenda-detail-header'>
        <Link to='/agendaitems' className='agenda-detail-back'>
          <BsArrowLeft aria-hidden='true' />
          {t('backToAgenda')}
        </Link>

        <div className='agenda-detail-heading'>
          <div className='agenda-detail-title-group'>
            <div className='agenda-detail-type'>
              <BsTag aria-hidden='true' />
              <MultiLanguageText
                nl={agendaItem.agendaitem_type?.name_nl}
                en={agendaItem.agendaitem_type?.name_en}
                fallback={t('header')}
              />
            </div>
            <h1>
              <MultiLanguageText nl={agendaItem.name_nl} en={agendaItem.name_en} />
            </h1>
          </div>

          <div className='agenda-detail-actions'>
            <Can I='edit' this={subject('Agendaitem', agendaItem)}>
              <Button
                variant='outline-primary'
                as={Link}
                to={`/agendaitems/${id}/edit`}
              >
                <BsPencil aria-hidden='true' />
                {tGeneric('edit')}
              </Button>
            </Can>
            <Can I='delete' this={subject('Agendaitem', agendaItem)}>
              <Button variant='outline-danger' onClick={onClickRemove}>
                <BsTrash aria-hidden='true' />
                {tGeneric('remove')}
              </Button>
            </Can>
          </div>
        </div>
      </header>

      <div className={`agenda-detail-layout ${agendaItem.can_subscribe ? 'agenda-detail-layout-has-subscriptions' : 'agenda-detail-layout-no-subscriptions'}`}>
        <div className='agenda-detail-main'>
          <section className='agenda-detail-facts' aria-label={t('eventDetails')}>
            <div className='agenda-detail-fact agenda-detail-fact-date'>
              <span className='agenda-detail-fact-icon'><BsCalendar3 aria-hidden='true' /></span>
              <div>
                <span className='agenda-detail-fact-label'>{t('dateAndTime')}</span>
                <time dateTime={agendaItem.date}>
                  <strong>{format(date, 'EEEE, PPP', lang)}</strong>
                  <span>{format(date, 'p', lang)}</span>
                </time>
              </div>
            </div>
            {agendaItem.location && (
              <div className='agenda-detail-fact'>
                <span className='agenda-detail-fact-icon'><BsGeoAlt aria-hidden='true' /></span>
                <div>
                  <span className='agenda-detail-fact-label'>{t('location')}</span>
                  <strong>{agendaItem.location}</strong>
                </div>
              </div>
            )}
            {agendaItem.committee && (
              <div className='agenda-detail-fact'>
                <span className='agenda-detail-fact-icon'><BsTag aria-hidden='true' /></span>
                <div>
                  <span className='agenda-detail-fact-label'>{t('committee')}</span>
                  <strong>
                    <MultiLanguageText
                      nl={agendaItem.committee.name_nl}
                      en={agendaItem.committee.name_en}
                    />
                  </strong>
                </div>
              </div>
            )}
            {eventUrl && (
              <div className='agenda-detail-fact'>
                <span className='agenda-detail-fact-icon'><BsLink45Deg aria-hidden='true' /></span>
                <div>
                  <span className='agenda-detail-fact-label'>{t('website')}</span>
                  <a href={eventUrl} target='_blank' rel='noopener noreferrer'>
                    {agendaItem.url}
                  </a>
                </div>
              </div>
            )}
          </section>

          <section className='agenda-detail-description'>
            <div className='agenda-detail-section-heading'>
              <span className='agenda-detail-section-icon'><BsClock aria-hidden='true' /></span>
              <h2>{t('aboutEvent')}</h2>
            </div>
            <div className='agenda-detail-prose'>
              <MultiLanguageText
                nl={agendaItem.description_nl}
                en={agendaItem.description_en}
                renderFunction={renderDescription}
              />
            </div>
          </section>

        </div>

        {agendaItem.can_subscribe && (
          <aside className='agenda-detail-sidebar'>
            <Can I='view' a='User' passThrough>
              {allowed => <SubscriptionsCard agendaItem={agendaItem} allowed={allowed} />}
            </Can>
          </aside>
        )}
      </div>
    </article>
  )
}

export default AgendaItem
