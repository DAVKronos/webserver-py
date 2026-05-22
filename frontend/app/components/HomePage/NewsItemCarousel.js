import React from 'react'
import { Carousel } from 'react-bootstrap'
import { getAPIHostUrl } from '../../utils/rest-helper'
import { useTranslation } from 'react-i18next'
import MultiLanguageText from '../Generic/MultiLanguageText'

const NewsItemCarousel = ({ items }) => {
  const { i18n } = useTranslation('homepage')

  if (!items || items.length === 0) {
    return null
  }

  const validItems = items.filter(item => item?.photo_file?.file_name)

  return (
    <Carousel pause={false} interval={10000}>
      {validItems.map(item => (
        <Carousel.Item key={item.id}>
          <img
            className='d-block w-100'
            src={`/static/newsitem_photos/${item.photo_file.file_name}`}
            alt={item.title_en}
          />
          <Carousel.Caption>
            <h3>
              <MultiLanguageText
                nl={item.title_nl}
                en={item.title_en}
              />
            </h3>
          </Carousel.Caption>
        </Carousel.Item>
      ))}
    </Carousel>
  )
}

export default NewsItemCarousel