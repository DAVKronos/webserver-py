import React, { useMemo, useState } from 'react'
import { useQuery } from 'react-query'
import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { format } from '../../utils/date-format'
import DefaultSpinner from '../Generic/Spinner'
import { getUserBirthdays } from './queries'

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

const UserBirthdays = () => {
  const { i18n, t } = useTranslation('homepage')
  const [currentMonth] = useState(() => {
    const today = new Date()
    return new Date(today.getFullYear(), today.getMonth(), 1)
  })
  const [selectedDate, setSelectedDate] = useState(() => new Date())
  const year = currentMonth.getFullYear()
  const month = currentMonth.getMonth()
  const { isLoading, isError, data, error, refetch } = useQuery(
    ['user_birthdays', month + 1],
    () => getUserBirthdays(month + 1)
  )
  const birthdays = data || EMPTY_BIRTHDAYS
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

  const monthName = new Intl.DateTimeFormat(i18n.language, {
    month: 'long',
    year: 'numeric'
  }).format(currentMonth)
  const firstWeekday = (new Date(year, month, 1).getDay() + 6) % 7
  const daysInMonth = new Date(year, month + 1, 0).getDate()
  const today = new Date()
  const calendarDays = Array.from({ length: 42 }, (_, index) => {
    const day = index - firstWeekday + 1
    return day > 0 && day <= daysInMonth ? day : null
  })
  const weekdays = Array.from({ length: 7 }, (_, index) => {
    const weekday = new Date(2024, 0, 1 + index)
    return new Intl.DateTimeFormat(i18n.language, { weekday: 'short' }).format(weekday)
  })
  const selectedBirthdays = selectedDate.getFullYear() === year &&
    selectedDate.getMonth() === month
    ? birthdaysByDay[selectedDate.getDate()] || []
    : []

  const selectDay = day => {
    if (day !== null) {
      setSelectedDate(new Date(year, month, day))
    }
  }

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

  const renderBirthdayLink = user => (
    <Link className='birthday-person' key={user.id} to={`/users/${user.id}`}>
      <span className='birthday-person-icon'><CakeIcon /></span>
      <span>{user.name}</span>
    </Link>
  )

  return (
    <section className='birthday-calendar' aria-labelledby='birthday-calendar-title'>
      <header className='birthday-calendar-header'>
        <div className='birthday-calendar-heading'>
          <span className='birthday-calendar-eyebrow'>
            <svg className='birthday-calendar-sparkle' viewBox='0 0 24 24' aria-hidden='true'>
              <path d='m12 2 1.8 7.2L21 12l-7.2 1.8L12 21l-1.8-7.2L3 12l7.2-2.8L12 2Z' />
            </svg>
            {t('birthdays')}
          </span>
          <h2 id='birthday-calendar-title'>{t('birthdayCalendarTitle')}</h2>
          <p>{t('birthdayCalendarSubtitle')}</p>
        </div>
      </header>

      <div className='birthday-calendar-month-title'>
        <h3>{monthName}</h3>
        <span>
          {monthBirthdays.length === 1
            ? t('oneBirthdayThisMonth')
            : t('birthdaysThisMonth', { count: monthBirthdays.length })}
        </span>
      </div>

      <div className='birthday-calendar-layout'>
        <div className='birthday-calendar-main'>
          <div className='birthday-calendar-weekdays' aria-hidden='true'>
            {weekdays.map((weekday, index) => (
              <span key={`${weekday}-${index}`}>{weekday}</span>
            ))}
          </div>
          <div className='birthday-calendar-grid' role='group' aria-label={monthName}>
            {calendarDays.map((day, index) => {
              if (day === null) {
                return <div className='birthday-calendar-day is-empty' key={`empty-${index}`} aria-hidden='true' />
              }

              const dayBirthdays = birthdaysByDay[day] || []
              const date = new Date(year, month, day)
              const isSelected = selectedDate.getFullYear() === year &&
                selectedDate.getMonth() === month &&
                selectedDate.getDate() === day
              const isToday = today.getFullYear() === year &&
                today.getMonth() === month &&
                today.getDate() === day

              return (
                <button
                  type='button'
                  className={`birthday-calendar-day${isSelected ? ' is-selected' : ''}${isToday ? ' is-today' : ''}${dayBirthdays.length ? ' has-birthdays' : ''}`}
                  key={day}
                  onClick={() => selectDay(day)}
                  onKeyDown={event => handleDayKeyDown(event, day)}
                  aria-label={`${format(date, 'EEEE, PPP', i18n.language)}${dayBirthdays.length
                    ? `. ${dayBirthdays.length} ${t('birthdays')}: ${dayBirthdays.map(user => user.name).join(', ')}`
                    : ''}`}
                  aria-pressed={isSelected}
                >
                  <span className='birthday-calendar-date'>{day}</span>
                  <span className='birthday-calendar-day-entries'>
                    {dayBirthdays.slice(0, 2).map(user => (
                      <span className='birthday-calendar-day-entry' key={user.id}>
                        <CakeIcon />
                        <span>{user.name.split(' ')[0]}</span>
                      </span>
                    ))}
                    {dayBirthdays.length > 2 && (
                      <span className='birthday-calendar-day-overflow'>
                        {t('moreBirthdayPeople', { count: dayBirthdays.length - 2 })}
                      </span>
                    )}
                  </span>
                </button>
              )
            })}
          </div>
        </div>

        <aside className='birthday-calendar-sidebar'>
          <section className='birthday-selected-day' aria-live='polite'>
            <span className='birthday-panel-label'>{t('selectedDay')}</span>
            <h4>{format(selectedDate, 'EEEE, d MMMM', i18n.language)}</h4>
            {selectedBirthdays.length
              ? <div className='birthday-selected-list'>{selectedBirthdays.map(renderBirthdayLink)}</div>
              : <p className='birthday-empty-message'>{t('noBirthdaysOnDay')}</p>}
          </section>

          <section className='birthday-month-list'>
            <h4>{t('monthBirthdays')}</h4>
            {isLoading && <div className='birthday-calendar-loading'><DefaultSpinner /></div>}
            {isError && (
              <div className='birthday-calendar-error' role='alert'>
                <p>{t('birthdaysLoadError')}</p>
                {error?.message && <p className='birthday-calendar-error-detail'>{error.message}</p>}
                <button type='button' onClick={() => refetch()}>{t('retry')}</button>
              </div>
            )}
            {!isLoading && !isError && (monthBirthdays.length
              ? <div className='birthday-month-list-items'>{monthBirthdays.map(user => {
                const day = getBirthdayDay(user.birthdate, year)
                const birthdayDate = new Date(year, month, day)
                return (
                  <button
                    type='button'
                    className='birthday-month-list-item'
                    key={user.id}
                    onClick={() => selectDay(day)}
                  >
                    <span className='birthday-month-list-date'>
                      {format(birthdayDate, 'd MMM', i18n.language)}
                    </span>
                    <span className='birthday-month-list-name'>{user.name}</span>
                    <span className='birthday-month-list-icon'><CakeIcon /></span>
                  </button>
                )
              })}</div>
              : <p className='birthday-empty-message'>{t('noBirthdaysThisMonth')}</p>)}
          </section>
        </aside>
      </div>
    </section>
  )
}

export default UserBirthdays
