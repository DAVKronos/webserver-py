import React, { useState, useContext } from 'react'
import { Button, Col, Row, Image, Form } from 'react-bootstrap'
import { format } from '../../utils/date-format'
import { useQuery, useQueryCache } from 'react-query'

import {
  approveNewsItem,
  createNewsItemComment,
  getUnapprovedNewsItem,
  getNewsItem,
  getNewsItemComments,
  removeNewsItem,
  removeNewsItemComment
} from './queries'

import DefaultSpinner from '../Generic/Spinner'
import AdminCard from '../Generic/AdminCard'
import { Can } from '../../utils/auth-helper'
import { useTranslation } from 'react-i18next'
import { Link, useHistory } from 'react-router-dom'
import Markdown from '../Generic/Markdown'
import { subject } from '@casl/ability'
import { authContext } from '../../utils/AuthContext'
import RemoveButton from '../Generic/RemoveButton'

/* ---------------- COMMENTS ---------------- */

const NewsItemComments = ({ newsItemId }) => {
  const { isLoading, data: comments } = useQuery(
    ['comments', newsItemId],
    getNewsItemComments
  )

  return (
    <div>
      {comments?.map(comment => (
        <Comment key={comment.id} comment={comment} />
      ))}

      <Can I="create" a="Comment">
        {!isLoading && <NewComment newsItemId={newsItemId} />}
      </Can>
    </div>
  )
}

/* ---------------- NEW COMMENT ---------------- */

const NewComment = ({ newsItemId }) => {
  const { user } = useContext(authContext)
  const [loading, setLoading] = useState(false)
  const [text, setText] = useState('')
  const { t } = useTranslation('generic')
  const queryCache = useQueryCache()

  const createComment = () => {
    setLoading(true)

    const comment = {
      newsitem_id: newsItemId,
      content: text
    }

    createNewsItemComment(newsItemId, comment)
      .then(() => {
        queryCache.invalidateQueries(['comments', newsItemId])
        setText('')
      })
      .finally(() => setLoading(false))
  }

  return (
    <Row style={{ borderTop: '1px solid #eee', paddingTop: 10 }}>
      <Col md={2} className="text-center">
        {user && (
          <>
            <Image src={user.avatar_file?.path} roundedCircle />
            <h5>{user.name}</h5>
          </>
        )}
      </Col>

      <Col md={8}>
        <Form.Control
          as="textarea"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder={t('comment')}
        />
      </Col>

      <Col md={2}>
        <Button variant="success" onClick={createComment} disabled={loading}>
          {loading ? <DefaultSpinner inline /> : t('send')}
        </Button>
      </Col>
    </Row>
  )
}

/* ---------------- COMMENT ---------------- */

const Comment = ({ comment }) => {
  const { t } = useTranslation('generic')
  const queryCache = useQueryCache()

  const onClickRemove = () => {
    removeNewsItemComment(comment.id).then(() => {
      queryCache.invalidateQueries(['comments', comment.newsitem_id])
    })
  }

  return (
    <Row style={{ borderTop: '1px solid #eee', paddingTop: 10 }}>
      <Col md={2} className="text-center">
        {comment.user && (
          <>
            <Image src={comment.user.avatar_file?.path} roundedCircle />
            <h5>{comment.user.name}</h5>
          </>
        )}
      </Col>

      <Col md={8}>
        {comment.content}
      </Col>

      <Col md={2}>
        <Can I="destroy" this={subject('Comment', comment)}>
          <RemoveButton variant="danger" onRemove={onClickRemove}>
            {t('remove')}
          </RemoveButton>
        </Can>
      </Col>
    </Row>
  )
}

/* ---------------- NEWS ITEM  ---------------- */

function NewsItem(props) {
  const { t, i18n } = useTranslation('generic')
  const history = useHistory()
  const queryCache = useQueryCache()

  const id = parseInt(props.match.params.id)
  const isUnapproved = props.match.url.includes('unapproved')

  const fetcher = isUnapproved ? getUnapprovedNewsItem : getNewsItem

  const { isLoading, isError, data, error } = useQuery(
    ['newsitems', id],
    fetcher
  )

  if (isLoading) return <DefaultSpinner />
  if (isError) return <div>Error: {error.message}</div>
  if (!data) return null

  const item = data

  const isDutch = i18n.language.startsWith('nl')
  const getLocalized = (nl, en) => (isDutch ? nl : (en || nl))

  const title = getLocalized(item.title_nl, item.title_en)
  const news = getLocalized(item.content_nl, item.content_en)

  const onClickRemove = () => {
    removeNewsItem(id).then(() => {
      history.goBack()
    })
  }

  const onClickApprove = () => {
    approveNewsItem(id).then(() => {
      queryCache.invalidateQueries(['newsitems'])
      history.push('/admin/approve-news')
    })
  }

  return (
    <>
      <Row>
        <Col md={{ span: 8, offset: 2 }}>
          <img src={item.photo_file?.path} alt={title} className='d-block' style={{ maxWidth: '100%' }} />
          <div className='kronos-header'>
            <h1>{title}</h1>
          </div>
          <div className='page-content'>
            <h6 className='green'>
              {format(item.created_at, 'PPP p', i18n.language)} |{' '}
              {item.creator?.name || 'Unknown'}
            </h6>
            <Markdown>{news}</Markdown>

            <Can I="read" a="Comment">
              <NewsItemComments newsItemId={item.id} />
            </Can>
          </div>
        </Col>

        <Col md={2}>
          {/* Only shown to people who may edit news items */}
          <Can I="update" a="Newsitem">
            <AdminCard>
              {!item.approved && (
                <Can I="manage" subject="all">
                  <Button variant="success" block onClick={onClickApprove}>
                    {t('approve')}
                  </Button>
                </Can>
              )}
              <Button variant="warning" block as={Link} to={`/newsitems/${id}/edit`}>
                {t('edit')}
              </Button>
              <Can I="destroy" a="Newsitem">
                <RemoveButton variant="danger" block onRemove={onClickRemove}>
                  {t('remove')}
                </RemoveButton>
              </Can>
            </AdminCard>
          </Can>
        </Col>
      </Row>

      <Row>
        <Col md={8}>
          
          
        </Col>
      </Row>
    </>
  )
}

export default NewsItem