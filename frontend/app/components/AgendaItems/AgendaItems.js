import React, { useEffect, useMemo, useState } from 'react'
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
import { getUserBirthdays } from '../HomePage/queries'

const EMPTY_BIRTHDAYS = []

const CakeIcon = () => (
  <svg viewBox='0 0 24 24' aria-hidden='true' focusable='false'>
    <path d='M4 13h16v7H4zM3 20h18M7 13V9m5 4V9m5 4V9M7 7c0-1 .8-1.5.8-2.5M12 7c0-1 .8-1.5.8-2.5M17 7c0-1 .8-1.5.8-2.5M4 16h2m4 0h2m4 0h2' />
  </svg>
)

function getBirthdayDay (birthdate, year) {
  if (typeof birthdate !== 'string') {
    return null
  }

  const [, month, day] = birthdate.split('-').map(Number)
  const isUnobservedLeapDay = month === 2 &&
    day === 29 &&
    new Date(year, 1, 29).getMonth() !== 1
  if (isUnobservedLeapDay) {
    return null
  }

  return month >= 1 && month <= 12 && day >= 1 && day <= 31
    ? day
    : null
}

function BirthdayData ({ month, onData }) {
  const query = useQuery(
    ['user_birthdays', month],
    () => getUserBirthdays(month)
  )

  useEffect(() => {
    onData({
      birthdays: query.data || EMPTY_BIRTHDAYS,
      isLoading: query.isLoading,
      isError: query.isError,
      error: query.error,
      refetch: query.refetch
    })
  }, [query.data, query.isLoading, query.isError, query.error, query.refetch, onData])

  return null
}

const AgendaItems = () => {
  const { search } = useLocation()
  const { t, i18n } = useTranslation('generic')
  const { t: tBirthday } = useTranslation('homepage')
  const lang = i18n.language
  const queryParams = parseParams(search)
  const date = queryParams.year && queryParams.month
    ? new Date(queryParams.year, queryParams.month - 1)
    : new Date()
  const year = date.getFullYear()
  const month = date.getMonth()
  const [selectedDate, setSelectedDate] = useState(() => {
    const today = new Date()
    return today.getFullYear() === year && today.getMonth() === month
      ? today
      : date
  })
  const [birthdayQuery, setBirthdayQuery] = useState({
    birthdays: EMPTY_BIRTHDAYS,
    isLoading: false,
    isError: false,
    error: null,
    refetch: null
  })

  const {
    isLoading,
    isError,
    data: agendaItems = [],
    refetch
  } = useQuery(
    ['agendaitems', { year, month }],
    getAgendaitems
  )
  const birthdays = birthdayQuery.birthdays
  const upcomingQuery = useQuery(
    ['agendaitems', 'upcoming'],
    () => {
      const now = new Date()
      const months = [0, 1, 2].map(offset => new Date(
        now.getFullYear(),
        now.getMonth() + offset
      ))
      return Promise.all(months.map(monthDate => getAgendaitems(null, {
        year: monthDate.getFullYear(),
        month: monthDate.getMonth()
      }))).then(monthItems => monthItems.flat())
    }
  )
  const monthBirthdays = useMemo(
    () => birthdays.filter(user => getBirthdayDay(user.birthdate, year) !== null),
    [birthdays, year]
  )
  const birthdaysByDay = useMemo(() => {
    return monthBirthdays.reduce((grouped, user) => {
      const day = getBirthdayDay(user.birthdate, year)
      if (day !== null) {
        grouped[day] = [...(grouped[day] || []), user]
      }
      return grouped
    }, {})
  }, [monthBirthdays, year])
  const eventsByDay = useMemo(() => {
    return agendaItems.reduce((grouped, item) => {
      const itemDate = new Date(item.date)
      if (itemDate.getFullYear() === year && itemDate.getMonth() === month) {
        const day = itemDate.getDate()
        grouped[day] = [...(grouped[day] || []), item]
      }
      return grouped
    }, {})
  }, [agendaItems, year, month])
  const upcomingEvents = useMemo(() => {
    const now = new Date()
    now.setHours(0, 0, 0, 0)
    return (upcomingQuery.data || [])
      .filter(item => {
        const typeName = item.agendaitem_type?.name_nl || ''
        return !typeName.toLowerCase().includes('training') &&
          new Date(item.date) >= now
      })
      .sort((a, b) => new Date(a.date) - new Date(b.date))
      .slice(0, 3)
  }, [upcomingQuery.data])
  const upcomingEventIds = useMemo(
    () => new Set(upcomingEvents.map(item => item.id)),
    [upcomingEvents]
  )

  const daysInMonth = new Date(year, month + 1, 0).getDate()
  const firstWeekday = (new Date(year, month, 1).getDay() + 6) % 7
  const calendarDays = Array.from({ length: 42 }, (_, index) => {
    const day = index - firstWeekday + 1
    return day > 0 && day <= daysInMonth ? day : null
  })
  const weekdays = Array.from({ length: 7 }, (_, index) => (
    new Intl.DateTimeFormat(lang, { weekday: 'short' }).format(new Date(2024, 0, 1 + index))
  ))
  const selectedCalendarDate = selectedDate.getFullYear() === year && selectedDate.getMonth() === month
    ? selectedDate
    : new Date(year, month, 1)
  const selectedEvents = eventsByDay[selectedCalendarDate.getDate()] || []
  const selectedBirthdays = birthdaysByDay[selectedCalendarDate.getDate()] || []
  const today = new Date()

  const handleDayKeyDown = (event, day) => {
    const offsets = {
      ArrowLeft: -1,
      ArrowRight: 1,
      ArrowUp: -7,
      ArrowDown: 7
    }
    const offset = offsets[event.key]
    if (!offset) {
      return
    }

    event.preventDefault()
    const nextDay = Math.max(1, Math.min(daysInMonth, day + offset))
    setSelectedDate(new Date(year, month, nextDay))
  }

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

        <Can I='view' a='User'>
          <BirthdayData month={month + 1} onData={setBirthdayQuery} />
        </Can>

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

        {!isLoading && (
          <div className='agenda-calendar-layout'>
            <div className='agenda-calendar-main'>
              <div className='agenda-calendar-weekdays' aria-hidden='true'>
                {weekdays.map((weekday, index) => (
                  <span key={`${weekday}-${index}`}>{weekday}</span>
                ))}
              </div>
              <div className='agenda-calendar-grid' role='group' aria-label={format(date, 'MMMM yyyy', lang)}>
                {calendarDays.map((day, index) => {
                  if (day === null) {
                    return <div className='agenda-calendar-day is-empty' key={`empty-${index}`} aria-hidden='true' />
                  }

                  const dayEvents = eventsByDay[day] || []
                  const dayBirthdays = birthdaysByDay[day] || []
                  const dayDate = new Date(year, month, day)
                  const isSelected = selectedCalendarDate.getDate() === day
                  const isToday = today.getFullYear() === year &&
                    today.getMonth() === month &&
                    today.getDate() === day
                  const entries = [
                    ...dayEvents.map(item => ({ type: 'event', item })),
                    ...dayBirthdays.map(user => ({ type: 'birthday', user }))
                  ]
                  const dayLabel = [
                    dayEvents.length
                      ? t('agendaItemPage:eventCount', { count: dayEvents.length })
                      : '',
                    dayBirthdays.length
                      ? `${dayBirthdays.length} ${tBirthday('birthdays')}: ${dayBirthdays.map(user => user.name).join(', ')}`
                      : ''
                  ].filter(Boolean).join('. ')

                  return (
                    <button
                      type='button'
                      className={`agenda-calendar-day${isSelected ? ' is-selected' : ''}${isToday ? ' is-today' : ''}${entries.length ? ' has-items' : ''}`}
                      key={day}
                      onClick={() => setSelectedDate(dayDate)}
                      onKeyDown={event => handleDayKeyDown(event, day)}
                      aria-label={`${format(dayDate, 'EEEE, PPP', lang)}${dayLabel ? `. ${dayLabel}` : ''}`}
                      aria-pressed={isSelected}
                    >
                      <span className='agenda-calendar-date'>{day}</span>
                      <span className='agenda-calendar-day-entries'>
                        {entries.slice(0, 2).map(entry => entry.type === 'event'
                          ? (
                            <span
                              className={`agenda-calendar-day-entry is-event${upcomingEventIds.has(entry.item.id) ? ' is-upcoming' : ''}`}
                              key={`event-${entry.item.id}`}
                            >
                              <span className='agenda-calendar-entry-name'>
                                <MultiLanguageText nl={entry.item.name_nl} en={entry.item.name_en} />
                              </span>
                            </span>
                          )
                          : (
                            <span className='agenda-calendar-day-entry is-birthday' key={`birthday-${entry.user.id}`}>
                              <CakeIcon />
                              <span>{entry.user.name.split(' ')[0]}</span>
                            </span>
                          ))}
                        {entries.length > 2 && (
                          <span className='agenda-calendar-day-overflow'>
                            {t('agendaItemPage:moreItems', { count: entries.length - 2 })}
                          </span>
                        )}
                      </span>
                    </button>
                  )
                })}
              </div>
            </div>

            <aside className='agenda-calendar-sidebar'>
              {upcomingEvents.length > 0 && (
                <section className='agenda-upcoming-events' aria-labelledby='agenda-upcoming-heading'>
                  <span className='agenda-panel-label'>{t('agendaItemPage:monthSchedule')}</span>
                  <h3 id='agenda-upcoming-heading'>{t('agendaItemPage:upcomingEvents')}</h3>
                  <div className='agenda-upcoming-list'>
                    {upcomingEvents.map((item, index) => {
                      const itemDate = new Date(item.date)
                      return (
                        <Link
                          key={item.id}
                          to={`/agendaitems/${item.id}`}
                          className={`agenda-upcoming-event${index === 0 ? ' is-next' : ''}`}
                        >
                          <span className='agenda-upcoming-date'>
                            <span>{format(itemDate, 'd', lang)}</span>
                            <small>{format(itemDate, 'MMM', lang)}</small>
                          </span>
                          <span className='agenda-upcoming-name'>
                            <MultiLanguageText nl={item.name_nl} en={item.name_en} />
                          </span>
                        </Link>
                      )
                    })}
                  </div>
                </section>
              )}
              <section className='agenda-selected-day' aria-live='polite'>
                <span className='agenda-panel-label'>{tBirthday('selectedDay')}</span>
                <h3>{format(selectedCalendarDate, 'EEEE, d MMMM', lang)}</h3>
                {selectedEvents.length
                  ? (
                    <div className='agenda-selected-events'>
                      {selectedEvents.map(item => {
                        const itemDate = new Date(item.date)
                        return (
                          <Link
                            key={item.id}
                            to={`/agendaitems/${item.id}`}
                            className={`agenda-selected-event${upcomingEventIds.has(item.id) ? ' is-upcoming' : ''}`}
                          >
                            {item.agendaitem_type && (
                              <span className='agenda-selected-event-type'>
                                <AgendaItemTypeName agendaItemType={item.agendaitem_type} />
                              </span>
                            )}
                            <span className='agenda-selected-event-title'>
                              <MultiLanguageText nl={item.name_nl} en={item.name_en} />
                            </span>
                            <span className='agenda-selected-event-details'>
                              <span><BsClock aria-hidden='true' />{format(itemDate, 'p', lang)}</span>
                              {item.location && <span><BsGeoAlt aria-hidden='true' />{item.location}</span>}
                              {Array.isArray(item.subscriptions) && (
                                <span>
                                  <BsPeople aria-hidden='true' />
                                  {t('agendaItemPage:subscriptions.count', { count: item.subscriptions.length })}
                                </span>
                              )}
                            </span>
                          </Link>
                        )
                      })}
                    </div>
                  )
                  : <p className='agenda-calendar-empty-message'>{t('agendaItemPage:noEventsOnDay')}</p>}

                <h4 className='agenda-selected-birthday-title'>{tBirthday('birthdays')}</h4>
                {selectedBirthdays.length
                  ? (
                    <div className='agenda-selected-birthdays'>
                      {selectedBirthdays.map(user => (
                        <Link className='agenda-birthday-person' key={user.id} to={`/users/${user.id}`}>
                          <span className='agenda-birthday-icon'><CakeIcon /></span>
                          <span>{user.name}</span>
                        </Link>
                      ))}
                    </div>
                  )
                  : <p className='agenda-calendar-empty-message'>{tBirthday('noBirthdaysOnDay')}</p>}
              </section>

              {birthdayQuery.isError && (
                <Alert variant='danger' className='agenda-calendar-error' role='alert'>
                  <p>{tBirthday('birthdaysLoadError')}</p>
                  {birthdayQuery.error?.message && (
                    <p className='agenda-calendar-error-detail'>{birthdayQuery.error.message}</p>
                  )}
                  <Button variant='outline-danger' onClick={() => birthdayQuery.refetch()}>
                    {tBirthday('retry')}
                  </Button>
                </Alert>
              )}
            </aside>
          </div>
        )}
      </section>
    </div>
  )
}

export default AgendaItems
