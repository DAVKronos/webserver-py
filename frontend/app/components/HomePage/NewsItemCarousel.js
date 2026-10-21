import React, { useEffect, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { Link } from 'react-router-dom'
import { format } from '../../utils/date-format'
import MultiLanguageText from '../Generic/MultiLanguageText'
import ReactMarkdown from 'react-markdown'
import placeholderImage from '../../images/image-thumb-placeholder.png'

const SLIDE_DURATION = 7000

const NewsItemCarousel = ({ items }) => {
  const { i18n, t } = useTranslation('homepage')
  const [activeIndex, setActiveIndex] = useState(0)
  const [isHovered, setIsHovered] = useState(false)
  const [isFocused, setIsFocused] = useState(false)
  const [prefersReducedMotion, setPrefersReducedMotion] = useState(() => (
    typeof window !== 'undefined' &&
    typeof window.matchMedia === 'function' &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches
  ))
  const featuredItems = (items || []).filter(item => item?.photo_file?.path)
  const currentIndex = featuredItems.length
    ? activeIndex % featuredItems.length
    : 0
  const currentItem = featuredItems[currentIndex]
  const isPaused = isHovered || isFocused || prefersReducedMotion

  useEffect(() => {
    if (typeof window.matchMedia !== 'function') {
      return undefined
    }

    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)')
    const updatePreference = event => setPrefersReducedMotion(event.matches)

    if (mediaQuery.addEventListener) {
      mediaQuery.addEventListener('change', updatePreference)
      return () => mediaQuery.removeEventListener('change', updatePreference)
    }

    mediaQuery.addListener(updatePreference)
    return () => mediaQuery.removeListener(updatePreference)
  }, [])

  useEffect(() => {
    if (featuredItems.length < 2 || isPaused) {
      return undefined
    }

    const timer = window.setTimeout(() => {
      setActiveIndex((currentIndex + 1) % featuredItems.length)
    }, SLIDE_DURATION)

    return () => window.clearTimeout(timer)
  }, [currentIndex, featuredItems.length, isPaused])

  if (!currentItem) {
    return null
  }

  const goTo = index => {
    setActiveIndex((index + featuredItems.length) % featuredItems.length)
  }

  const goToPrevious = () => goTo(currentIndex - 1)
  const goToNext = () => goTo(currentIndex + 1)

  return (
    <section
      className={`home-news-carousel${isPaused ? ' is-paused' : ''}`}
      role='region'
      aria-label={t('featuredNews')}
      aria-roledescription={t('carousel')}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      onFocus={() => setIsFocused(true)}
      onBlur={event => {
        if (!event.currentTarget.contains(event.relatedTarget)) {
          setIsFocused(false)
        }
      }}
    >
      <div className='home-news-carousel-content' aria-live='off'>
        <div className='home-news-carousel-kicker'>
          <Link to='/newsitems' aria-label={t('moreNews')}>
            {t('latestNews')}
            <span aria-hidden='true'>↗</span>
          </Link>
          <span className='home-news-carousel-count'>
            {String(currentIndex + 1).padStart(2, '0')} / {String(featuredItems.length).padStart(2, '0')}
          </span>
        </div>
        <article key={currentItem.id}>
          <h2>
            <Link to={`/newsitems/${currentItem.id}`}>
              <MultiLanguageText nl={currentItem.title_nl} en={currentItem.title_en} />
            </Link>
          </h2>
          <p className='home-news-carousel-meta'>
            {format(currentItem.created_at, 'PPP', i18n.language)}
            {currentItem.creator?.name ? ` · ${currentItem.creator.name}` : ''}
          </p>
          <div className='home-news-carousel-description'>
            <MultiLanguageText
              nl={currentItem.content_nl}
              en={currentItem.content_en}
              renderFunction={content => (
                <ReactMarkdown>{(content || '').split('\n')[0]}</ReactMarkdown>
              )}
            />
          </div>
          <Link className='home-news-carousel-read-more' to={`/newsitems/${currentItem.id}`}>
            {t('readMore')}
            <span aria-hidden='true'>↗</span>
          </Link>
        </article>

        <div className='home-news-carousel-controls'>
          <button
            type='button'
            className='home-news-carousel-control'
            onClick={goToPrevious}
            aria-label={t('previousStory')}
            disabled={featuredItems.length < 2}
          >
            <svg viewBox='0 0 24 24' aria-hidden='true'>
              <path d='M19 12H5m7 7-7-7 7-7' />
            </svg>
          </button>
          <button
            type='button'
            className='home-news-carousel-control'
            onClick={goToNext}
            aria-label={t('nextStory')}
            disabled={featuredItems.length < 2}
          >
            <svg viewBox='0 0 24 24' aria-hidden='true'>
              <path d='M5 12h14m-7-7 7 7-7 7' />
            </svg>
          </button>
        </div>
      </div>

      <div className='home-news-carousel-image'>
        <img
          key={currentItem.id}
          src={currentItem.photo_file?.path || placeholderImage}
          onError={event => {
            event.currentTarget.onerror = null
            event.currentTarget.src = placeholderImage
          }}
          alt=''
        />
      </div>

      {featuredItems.length > 1 && (
        <nav className='home-news-carousel-indicators' aria-label={t('chooseFeaturedNews')}>
          {featuredItems.map((item, index) => (
            <button
              key={item.id}
              type='button'
              className={`home-news-carousel-indicator${index === currentIndex ? ' active' : ''}`}
              onClick={() => setActiveIndex(index)}
              aria-label={t('showNewsStory', {
                title: i18n.language.startsWith('nl')
                  ? item.title_nl || item.title_en
                  : item.title_en || item.title_nl
              })}
              aria-current={index === currentIndex ? 'true' : undefined}
            >
              <span className='home-news-carousel-progress' aria-hidden='true'>
                <span />
              </span>
            </button>
          ))}
        </nav>
      )}
    </section>
  )
}

export default NewsItemCarousel