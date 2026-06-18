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
import { Can } from '../../utils/auth-helper'
import { useTranslation } from 'react-i18next'
import { Link, useHistory } from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import { subject } from '@casl/ability'
import { authContext } from '../../utils/AuthContext'

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
          <Button variant="danger" onClick={onClickRemove}>
            {t('remove')}
          </Button>
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
        <Col md={8}>
          <h1>{title}</h1>
          <p>
            {format(item.created_at, 'PPP p', i18n.language)} |{' '}
            {item.creator?.name || 'Unknown'}
          </p>
        </Col>

        <Col md={4} className="d-flex">
          {!item.approved && (
            <Can I="manage" subject="all">
              <Button variant="success" onClick={onClickApprove}>
                {t('approve')}
              </Button>
            </Can>
          )}

          <Can I="update" a="Newsitem">
            <Button
              variant="warning"
              as={Link}
              to={`/newsitems/${id}/edit`}
            >
              {t('edit')}
            </Button>
          </Can>

          <Can I="destroy" a="Newsitem">
            <Button variant="danger" onClick={onClickRemove}>
              {t('remove')}
            </Button>
          </Can>
        </Col>
      </Row>

      <Row>
        <Col md={8}>
          <img src={item.photo_file?.path} alt={title} style={{ maxWidth: '100%' }} />

          <ReactMarkdown>{news}</ReactMarkdown>

          <Can I="read" a="Comment">
            <NewsItemComments newsItemId={item.id} />
          </Can>
        </Col>
      </Row>
    </>
  )
}

export default NewsItem