import React, { useLayoutEffect, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { getLocalSettings, setLocalSettings } from '../../utils/local-settings'

function getInitialTheme () {
  const savedTheme = getLocalSettings('theme')
  if (savedTheme === 'dark' || savedTheme === 'light') {
    return savedTheme
  }

  return window.matchMedia?.('(prefers-color-scheme: dark)').matches
    ? 'dark'
    : 'light'
}

const ThemeToggle = () => {
  const [theme, setTheme] = useState(getInitialTheme)
  const { t } = useTranslation('navigation')
  const isDark = theme === 'dark'

  useLayoutEffect(() => {
    document.documentElement.dataset.theme = theme
    setLocalSettings('theme', theme)
  }, [theme])

  const toggleTheme = () => {
    const nextTheme = isDark ? 'light' : 'dark'
    document.documentElement.dataset.theme = nextTheme
    setTheme(nextTheme)
  }

  return (
    <div className='theme-toggle-item'>
      <button
        type='button'
        className={`theme-toggle${isDark ? ' is-dark' : ''}`}
        onClick={toggleTheme}
        aria-label={t(isDark ? 'switchToLightTheme' : 'switchToDarkTheme')}
        aria-pressed={isDark}
      >
        <span className='theme-toggle-track' aria-hidden='true'>
          <span className='theme-toggle-thumb'>
            {isDark
              ? <svg viewBox='0 0 24 24'><path d='M20.2 15.1A8.5 8.5 0 0 1 8.9 3.8 8.6 8.6 0 1 0 20.2 15.1Z' /></svg>
              : <svg viewBox='0 0 24 24'><circle cx='12' cy='12' r='4' /><path d='M12 2v2m0 16v2M4.93 4.93l1.42 1.42m11.3 11.3 1.42 1.42M2 12h2m16 0h2M4.93 19.07l1.42-1.42m11.3-11.3 1.42-1.42' /></svg>}
          </span>
          <span className='theme-toggle-icon theme-toggle-icon-sun'>
            <svg viewBox='0 0 24 24'><circle cx='12' cy='12' r='4' /><path d='M12 2v2m0 16v2M4.93 4.93l1.42 1.42m11.3 11.3 1.42 1.42M2 12h2m16 0h2M4.93 19.07l1.42-1.42m11.3-11.3 1.42-1.42' /></svg>
          </span>
          <span className='theme-toggle-icon theme-toggle-icon-moon'>
            <svg viewBox='0 0 24 24'><path d='M20.2 15.1A8.5 8.5 0 0 1 8.9 3.8 8.6 8.6 0 1 0 20.2 15.1Z' /></svg>
          </span>
        </span>
      </button>
    </div>
  )
}

export default ThemeToggle
