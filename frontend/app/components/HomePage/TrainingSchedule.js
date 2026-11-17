import React from 'react'
import { useTranslation } from 'react-i18next'

const TrainingSchedule = () => {
  const { t } = useTranslation('homepage')
  const days = [
    'monday',
    'tuesday',
    'wednesday',
    'thursday'
  ]

  return (
    <section className='training-schedule' aria-labelledby='training-schedule-title'>
      <h2 id='training-schedule-title'>{t('trainingSchedule')}</h2>
      <div className='training-schedule-timeline'>
        {days.map(day => (
          <article className='training-schedule-day' key={day}>
            <span className='training-schedule-marker' aria-hidden='true'>
              <span />
            </span>
            <h3>{t(`trainingDays.${day}`)}</h3>
            <p className='training-schedule-time'>{t('trainingTime')}</p>
            <ul>
              {t(`trainingDetails.${day}`, { returnObjects: true }).map(detail => (
                <li key={detail}>{detail}</li>
              ))}
            </ul>
          </article>
        ))}
      </div>
    </section>
  )
}

export default TrainingSchedule
