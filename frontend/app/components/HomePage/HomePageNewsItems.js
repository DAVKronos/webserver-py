import React from 'react'
import NewsItemCarousel from './NewsItemCarousel'
import { getNewsItems } from './queries'
import DefaultSpinner from '../Generic/Spinner'
import { useQuery } from 'react-query'
import { useTranslation } from 'react-i18next'
import { Can } from '../../utils/auth-helper'
import { Link } from 'react-router-dom'

const NewsItems = (props) => {
  const { isLoading, data } = useQuery('newsitems', getNewsItems)
  const { t } = useTranslation('generic')
  if (isLoading) {
    return <DefaultSpinner />
  }
  const newsItems = [...(data || [])].sort(sort_newsItems)
  const featuredItems = newsItems.slice(0, 4)

  return (
    <div className='home-news-feed'>
      <NewsItemCarousel items={featuredItems} />
      <Can I='create' a='Newsitem'>
        <Link className='btn btn-success' to='/newsitems/new'>
          {t('add')} {t('homepage:newsitem')}s
        </Link>
      </Can>
    </div>
  )
}

function sort_newsItems (a, b) {
  return new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
}

export default NewsItems
