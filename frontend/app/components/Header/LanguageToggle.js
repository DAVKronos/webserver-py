import React from 'react'
import { ButtonGroup, Button } from 'react-bootstrap'
import { useTranslation } from 'react-i18next'

// NL / ENG toggle: the active language is a filled green button, the other one outlined
const LanguageToggle = () => {
  const { i18n } = useTranslation()
  const isEnglish = i18n.language?.startsWith('en')

  return (
    <ButtonGroup className='language-toggle' aria-label='Language'>
      <Button
        variant={isEnglish ? 'outline-primary' : 'primary'}
        aria-pressed={!isEnglish}
        onClick={() => i18n.changeLanguage('nl')}
      >
        NL
      </Button>
      <Button
        variant={isEnglish ? 'primary' : 'outline-primary'}
        aria-pressed={isEnglish}
        onClick={() => i18n.changeLanguage('en')}
      >
        ENG
      </Button>
    </ButtonGroup>
  )
}

export default LanguageToggle
