import React from 'react'
import { Link, useHistory } from 'react-router-dom'
import { Button, Col, Image, Row } from 'react-bootstrap'
import { format } from '../../utils/date-format.js'
import { useTranslation } from 'react-i18next'
import ReactMarkdown from 'react-markdown'
import { BsFillChatTextFill } from 'react-icons/bs'
import MultiLanguageText from '../Generic/MultiLanguageText'
import { Can } from "../../utils/auth-helper"
import { approveNewsItem, removeNewsItem } from "./queries"

const ShortNewsItem = ({ item }) => {
    const { t, i18n } = useTranslation('newsItemPage')
    const history = useHistory()

    const renderNews = (news) => {
        return <ReactMarkdown>{news.split('\n')[0]}</ReactMarkdown>
    }

    let commentCount = null
    if (item.comment_count) {
        commentCount = <> | <BsFillChatTextFill /> {item.comment_count}</>
    }

    const onClickApprove = () => {
        approveNewsItem(item.id).then(() => {
            history.push('/admin/approve-news')
        })
    }

    const onClickRemove = () => {
        removeNewsItem(item.id).then(() => {
            history.goBack()
        })
    }

    const imageSrc = item.photo_file?.path?.trim() || null

    return (
        <Row>
            <Col md={3} style={{ display: 'flex' }}>
                <Link to={`/newsitems/${item.id}`} className='align-self-center'>

                    {imageSrc ? (
                        <Image
                            className='d-block w-100'
                            src={imageSrc}
                            alt={item.title}
                            thumbnail
                        />
                    ) : (
                        <div
                            className='d-flex align-items-center justify-content-center bg-light'
                            style={{ width: '100%', height: '150px' }}
                        >
                            No image
                        </div>
                    )}

                </Link>
            </Col>

            <Col md={9}>
                <header>
                    <Link to={`/newsitems/${item.id}`}>
                        <h2>
                            <MultiLanguageText
                                nl={item.title_nl}
                                en={item.title_en}
                            />
                        </h2>
                    </Link>

                    <p>
                        {format(item.created_at, 'PPP p', i18n.language)} |
                        {item.creator?.name || 'Unknown'}
                        {commentCount}
                    </p>
                </header>

                <div>
                    <MultiLanguageText
                        nl={item.news}
                        en={item.news_en}
                        renderFunction={renderNews}
                    />
                    <Link to={`/newsitems/${item.id}`}>
                        {t('readMore')}
                    </Link>
                </div>

                {!item.agreed && (
                    <Can I='manage' subject='all'>
                        <Button variant='success' onClick={onClickApprove}>
                            {t('approve')}
                        </Button>
                    </Can>
                )}

                <Can I='update' a='Newsitem'>
                    <Button
                        size='sm'
                        variant='warning'
                        as={Link}
                        to={`/newsitems/${item.id}/edit`}
                    >
                        {t('edit')}
                    </Button>
                </Can>

                <Can I='destroy' a='Newsitem'>
                    <Button
                        size='sm'
                        variant='danger'
                        onClick={onClickRemove}
                    >
                        {t('remove')}
                    </Button>
                </Can>
            </Col>

            <Col md={2}></Col>
        </Row>
    )
}

export default ShortNewsItem