import React from 'react'
import { Link, useHistory } from 'react-router-dom'
import { Button, Card, Col, Image, Row } from 'react-bootstrap'
import { format } from '../../utils/date-format.js'
import { useTranslation } from 'react-i18next'
import ReactMarkdown from 'react-markdown'
import { BsFillChatTextFill } from 'react-icons/bs'
import MultiLanguageText from '../Generic/MultiLanguageText'
import { Can } from "../../utils/auth-helper"
import { approveNewsItem, removeNewsItem } from "./queries"
import RemoveButton from '../Generic/RemoveButton'

const ShortNewsItem = ({ item }) => {
    const { t, i18n } = useTranslation('newsItemPage')
    const history = useHistory()

    // Preview: max. PREVIEW_LENGTH characters, cut at a whole word, with ... behind it
    const PREVIEW_LENGTH = 150
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
        <Card className='mb-3'>
            <Card.Body>
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
                                nl={item.content_nl}
                                en={item.content_en}
                                renderFunction={renderNews}
                            />
                            <div className='text-right'>
                                <Link to={`/newsitems/${item.id}`} className='btn btn-primary'>
                                    {t('readMore')}
                                </Link>
                            </div>
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
                            <RemoveButton
                                size='sm'
                                variant='danger'
                                onRemove={onClickRemove}
                            >
                                {t('remove')}
                            </RemoveButton>
                        </Can>
                    </Col>
                </Row>
            </Card.Body>
        </Card>
    )
}

export default ShortNewsItem
