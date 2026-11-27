import React from 'react'
import { Link } from 'react-router-dom'
import { Row, Col, Image, Card } from 'react-bootstrap'
import { format } from '../../utils/date-format.js'
import { useTranslation } from 'react-i18next'
import ReactMarkdown from 'react-markdown'
import { BsFillChatTextFill } from 'react-icons/bs'
import MultiLanguageText from '../Generic/MultiLanguageText'

const ShortNewsItem = ({ item }) => {
  const { t, i18n } = useTranslation('homepage')
  // Preview: max. PREVIEW_LENGTH characters, cut at a whole word, with ... behind it
  const PREVIEW_LENGTH = 500
  const renderNews = (news) => {
    const text = (news || '').replace(/\s+/g, ' ').trim()
    let preview = text
    if (text.length > PREVIEW_LENGTH) {
      const lastSpace = text.lastIndexOf(' ', PREVIEW_LENGTH)
      preview = text.slice(0, lastSpace > 0 ? lastSpace : PREVIEW_LENGTH) + '...'
    }
    return <ReactMarkdown>{preview}</ReactMarkdown>
  }
  let commentCount = null
  if (item.comment_count) {
    commentCount = <> | <BsFillChatTextFill /> {item.comment_count}</>
  }

  return (
    <Card className='mb-5'>
      {/* Image + header together form one link to the article */}
      <Link to={`/newsitems/${item.id}`} className='card-link d-block text-decoration-none'>
        <Card.Img variant="top" src={item.photo_file?.path} alt={item.title_nl} thumbnail/>
        <Card.Header className='kronos-header'>
          <h1><MultiLanguageText nl={item.title_nl} en={item.title_en} /></h1>
        </Card.Header>
      </Link>
      <Card.Body>
        <h6 className='green'>{format(item.created_at, 'PPP p', i18n.language)} | {item.creator?.name || 'Unknown'}{commentCount}</h6>
        <MultiLanguageText nl={item.content_nl} en={item.content_en} renderFunction={renderNews} />
        <div className='text-right'>
          <Link to={`/newsitems/${item.id}`} className='btn btn-primary stretched-link'>{t('readMore')}</Link>
        </div>
      </Card.Body>
    </Card>
  )
}

export default ShortNewsItem
