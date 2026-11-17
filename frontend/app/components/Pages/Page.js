import React from 'react'
import ReactMarkdown from 'react-markdown'
import { Button } from 'react-bootstrap'
import Spinner from '../Generic/Spinner'
import { useQuery } from 'react-query'
import { getPage, getPageByPageTag, removePage } from './queries'
import MultiLanguageText from '../Generic/MultiLanguageText'
import { Link, useHistory } from 'react-router-dom'
import { Can } from '../../utils/auth-helper'
import { subject } from '@casl/ability'
import { useTranslation } from 'react-i18next'

const PageComponent = ({ page, isLoading }) => {
  const { t, i18n } = useTranslation('generic')
  const history = useHistory()

  if (isLoading) {
    return <Spinner />
  }

  if (!page) {
    return <h1>Page not found</h1>
  }

  const isTrainingTimes = page.page_title_nl?.trim().toLowerCase() === 'trainingstijden'
  const fallbackTitle = isTrainingTimes
    ? (i18n.language.startsWith('nl') ? 'Trainingstijden' : 'Training times')
    : ''

  const renderMarkdown = (text) => {
    const components = isTrainingTimes
      ? {
          p: ({ children }) => {
            const paragraphText = getMarkdownText(children).trim()
            const firstChild = React.Children.toArray(children)[0]
            const classNames = ['training-times-paragraph']

            if (/^(monday|tuesday|wednesday|thursday|maandag|dinsdag|woensdag|donderdag)\b/i.test(paragraphText)) {
              classNames.push('training-times-day')
            } else if (/^(the general program|het algemene programma)\b/i.test(paragraphText)) {
              classNames.push('training-times-program')
            } else if (/^(all workouts|alle trainingen)\b/i.test(paragraphText)) {
              classNames.push('training-times-location')
            } else if (/^(note|let op|opmerking)\b/i.test(paragraphText)) {
              classNames.push('training-times-note')
            } else if (React.isValidElement(firstChild) && firstChild.type === 'strong') {
              classNames.push('training-times-topic')
            }

            return <p className={classNames.join(' ')}>{children}</p>
          }
        }
      : undefined

    const markdown = isTrainingTimes
        ? (text || '').replace(/(\*\*[^*\n]+\*\*):(?=\s)/g, '$1')
        : text || ''

    return <ReactMarkdown components={components}>{markdown}</ReactMarkdown>
  }

  const onClickRemove = () => {
    return removePage(page.id).then(() => {
	  history.push('/admin/pages')
    })
  }

  return (
    <div className={`cms-page${isTrainingTimes ? ' training-times-page' : ''}`}>
      <Can I='update' this={subject('Page', page)}>
        <Button
          variant='warning' className='align-self-center' as={Link}
          to={`/pages/${page.id}/edit`}
        >{t('edit')}
        </Button>
      </Can>
      <Can I='delete' this={subject('Page', page)}>
        <Button variant='danger' className='align-self-center' onClick={onClickRemove}>
          {t('remove')}
        </Button>
      </Can>

      <h1 className='cms-page-title'>
        <MultiLanguageText
          nl={page.page_title_nl || page.title_nl || fallbackTitle}
          en={page.page_title_en || page.title_en || fallbackTitle}
        />
      </h1>
      <div className={`cms-page-content${isTrainingTimes ? ' training-times-content' : ''}`}>
        <MultiLanguageText nl={page.content_nl} en={page.content_en} renderFunction={renderMarkdown} />
      </div>
    </div>
  )
}

function getMarkdownText (children) {
  return React.Children.toArray(children).map(child => {
    if (React.isValidElement(child)) {
      return getMarkdownText(child.props.children)
    }

    return child
  }).join('')
}

const Page = (props) => {
  const { id } = props.match.params
  const { isLoading, isError, data, error } = useQuery(['pages', id], getPage)

  return <PageComponent page={data} isLoading={isLoading} />
}

const PageWithTag = (props) => {
  const { page_title_nl } = props.match.params

  const { isLoading, data } = useQuery(
    ['pages', page_title_nl],
    () => getPageByPageTag(null, page_title_nl)
  )

  return <PageComponent page={data} isLoading={isLoading} />
}

export { Page, PageWithTag }
