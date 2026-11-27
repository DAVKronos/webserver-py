import React from 'react'
import Markdown from '../Generic/Markdown'
import { Button, Col, Row, Image, Form } from 'react-bootstrap'
import Spinner from '../Generic/Spinner'
import AdminCard from '../Generic/AdminCard'
import { useQuery } from 'react-query'
import { getPage, getPageByPageTag, removePage } from './queries'
import MultiLanguageText from '../Generic/MultiLanguageText'
import { Link, useHistory } from 'react-router-dom'
import { Can } from '../../utils/auth-helper'
import { subject } from '@casl/ability'
import { useTranslation } from 'react-i18next'
import RemoveButton from '../Generic/RemoveButton'

const PageComponent = ({ page, isLoading }) => {
  const { t, i18n } = useTranslation('generic')
  const lang = i18n.language
  const history = useHistory()

  if (isLoading) {
    return <Spinner />
  }

  if (!page) {
    return <h1>Page not found</h1>
  }

  const renderMarkdown = (text) => {
    return <Markdown>{text}</Markdown>
  }

  const onClickRemove = () => {
    return removePage(page.id).then(() => {
	  history.push('/admin/pages')
    })
  }

  return (
    <Row>
      <Col md={{ span: 8, offset: 2 }}>
      <div className='kronos-header'>
      <h1><MultiLanguageText nl={page.page_title_nl} en={page.page_title_en} /></h1></div>
      
      <div className='page-content'>
        <MultiLanguageText nl={page.content_nl} en={page.content_en} renderFunction={renderMarkdown} />
      </div>
      

      </Col>
      <Col md={2}>
        {/* Only shown to people who may edit this page */}
        <Can I='update' this={subject('Page', page)}>
          <AdminCard>
            <Button variant='warning' block as={Link} to={`/pages/${page.id}/edit`}>
              {t('edit')}
            </Button>
            <Can I='delete' this={subject('Page', page)}>
              <RemoveButton variant='danger' block onRemove={onClickRemove}>
                {t('remove')}
              </RemoveButton>
            </Can>
          </AdminCard>
        </Can>
      </Col>
    
    </Row>
  )
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
