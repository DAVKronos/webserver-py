import React, { useState, useContext } from 'react'
import { Button, Col, Row, Image, Form } from 'react-bootstrap'
import { getAPIHostUrl } from '../../utils/rest-helper'
import { format } from '../../utils/date-format'
import { useQuery, useQueryCache } from 'react-query'
import {
  approveNewsItem,
  createNewsItemComment,
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
import { getUser } from '../Users/queries'
import { subject } from '@casl/ability'
import { authContext } from '../../utils/AuthContext'

const NewsItemComments = ({ newsItemId }) => {
  const { isLoading, isError, data: comments, error } = useQuery(['comments', newsItemId], getNewsItemComments)

  return (
    <div>
      {comments && comments.map(comment => {
        return <Comment key={comment.id} comment={comment} />
      })}
      <Can I='create' a='Comment'>
        {!isLoading && <NewComment newsItemId={newsItemId} />}
      </Can>
    </div>
  )
}

const NewComment = ({ newsItemId }) => {
  const { user } = useContext(authContext)
  const [loading, setLoading] = useState(false)
  const [text, setText] = useState('')
  const { t } = useTranslation('generic')
  const queryCache = useQueryCache()

  const createComment = () => {
    setLoading(true)
    const comment = { commentable_id: newsItemId, commentable_type: 'Newsitem', commenttext: text }
    createNewsItemComment(newsItemId, comment).then(() => {
      queryCache.invalidateQueries(['comments', comment.commentable_id])
    }).finally(() => {
      setLoading(false)
    })
  }

  return (
    <Row style={{ borderTop: '1px solid #eee', paddingTop: 10, display: 'flex', alignItems: 'center' }}>
      <Col md={2} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        {user && <Image src={user.avatar_file.path} roundedCircle />}
        {user && <h5>{user.name}</h5>}
      </Col>
      <Col md={8} style={{ display: 'flex', alignItems: 'center' }}>
        <Form.Control as='textarea' value={text} onChange={e => setText(e.target.value)} placeholder={t('comment')} />
      </Col>
      <Col md={2}>

        <Button variant='success' onClick={createComment} disabled={loading}>
          {loading && <DefaultSpinner inline />}
          {!loading && t('send')}
        </Button>

      </Col>
    </Row>
  )
}

const Comment = ({ comment }) => {
  const commentUser = comment.user
  const { t } = useTranslation('generic')
  const queryCache = useQueryCache()
  const onClickRemove = () => {
    removeNewsItemComment(comment.commentable_id, comment.id).then(() => {
      queryCache.invalidateQueries(['comments', comment.commentable_id])
    })
  }
  return (
    <Row style={{ borderTop: '1px solid #eee', paddingTop: 10, display: 'flex', alignItems: 'center' }}>
      <Col md={2} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        {commentUser && <Image src={commentUser.avatar_file.path} roundedCircle />}
        {commentUser && <h5>{commentUser.name}</h5>}
      </Col>
      <Col md={8} style={{ display: 'flex', alignItems: 'center' }}>
        {comment.commenttext}
      </Col>
      <Col md={2}>
        <Can I='destroy' this={subject('Comment', comment)}>
          <Button variant='danger' onClick={onClickRemove}>{t('remove')}</Button>
        </Can>
      </Col>
    </Row>
  )
}



function NewsItem(props) {
  const { t, i18n } = useTranslation('generic')
  const history = useHistory()
  const id = parseInt(props.match.params.id, 10)

  const { isLoading, isError, data, error } = useQuery(['newsitems', id], getNewsItem)

  if (isLoading) {
    return <DefaultSpinner />
  }

  if (isError) {
    return <div>Error: {error.message}</div>
  }

  if (!data) return null

  const item = data

  const isDutch = i18n.language.startsWith('nl')
  const getLocalized = (nl, en) => (isDutch ? nl : (en || nl))

  const title = getLocalized(item.title_nl, item.title_en)
  const news = getLocalized(item.content_nl, item.content_en)

  const onClickRemove = async () => {
    try {
      await removeNewsItem(id)
      history.goBack()
    } catch (e) {
      console.error(e)
    }
  }

  const onClickApprove = async () => {
    try {
      await approveNewsItem(id)
      history.push('/admin/approve-news')
    } catch (e) {
      console.error(e)
    }
  }

  return (
    <>
      <Row>
        <Col md={{ span: 8, offset: 2 }}>
          <h1>{title}</h1>
          <p>
            {format(item.created_at, 'PPP p', i18n.language)} | {' '}
            {item.creator?.name || 'Unknown'}
          </p>
        </Col>
      </Row>

      <Row>
        <Col md={{ span: 8, offset: 2 }}>
          <img
            // src={getAPIHostUrl(item.photo_file.file_name)}
            src={`/static/newsitem_photos/${item.photo_file.file_name}`}
            alt={title}
          />

          <ReactMarkdown>
            {news}
          </ReactMarkdown>

          <Can I='read' a='Comment'>
            <NewsItemComments newsItemId={item.id} />
          </Can>
        </Col>

        <Col md={2}>
          {!item.approved && (
            <Can I='manage' subject='all'>
              <Button variant='success' onClick={onClickApprove}>
                {t('approve')}
              </Button>
            </Can>
          )}

          <Can I='update' a='Newsitem'>
            <Button
              variant='warning'
              as={Link}
              to={`/newsitems/${id}/edit`}
            >
              {t('edit')}
            </Button>
          </Can>

          <Can I='destroy' a='Newsitem'>
            <Button variant='danger' onClick={onClickRemove}>
              {t('remove')}
            </Button>
          </Can>
        </Col>
      </Row>
    </>
  )
}

export default NewsItem