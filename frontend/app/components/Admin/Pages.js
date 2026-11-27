import React from 'react'
import { useQuery, useQueryCache } from 'react-query'
import { Table, Button } from 'react-bootstrap'
import { getPages, removePage } from '../Pages/queries'
import { Link } from 'react-router-dom'
import { BsFillXCircleFill, BsFillCheckCircleFill, BsPlusLg } from 'react-icons/bs'
import { Can } from '../../utils/auth-helper'
import { useTranslation } from 'react-i18next'
import RemoveButton from '../Generic/RemoveButton'

const Pages = () => {
  const { isLoading, isError, data: pages, error } = useQuery('pages', getPages)
  const { t } = useTranslation('generic')
  const queryCache = useQueryCache()
  return (
    <>
      <h1>Informatie pagina&apos;s</h1>
      <Table striped>
        <thead>
          <tr>
            <th>
              Pagina titel (nl)
            </th>
            <th>
              Pagina titel (en)
            </th>
            <th>
              Menu
            </th>
            <th>
              Public
            </th>
            <th>
              Highlight
            </th>
            <th colSpan={3}>
              Acties
            </th>
          </tr>
        </thead>
        <tbody>
          {pages && pages.map(page => {
            const onClickRemove = () => {
              return removePage(page.id).then(() => {
                queryCache.invalidateQueries(['pages'], { exact: true })
              })
            }

            return (
              <tr key={page.id}>
                <td>{page.page_title_nl}</td>
                <td>{page.page_title_en}</td>
                <td>{page.menu_item}</td>
                <td>{page.is_public ? <BsFillCheckCircleFill /> : <BsFillXCircleFill />}</td>
                <td>{page.is_highlight ? <BsFillCheckCircleFill /> : <BsFillXCircleFill />}</td>
                <td><Link to={`/pages/${page.id}`}>Bekijk</Link></td>
                <td><Link to={`/pages/${page.id}/edit`}>Bewerk</Link></td>
                <td><RemoveButton variant='link' className='p-0 align-baseline' onRemove={onClickRemove}>Verwijder</RemoveButton></td>
              </tr>
            )
          })}
        </tbody>
      </Table>

      {/* New page button at the bottom; mb-5 keeps it away from the footer */}
      <Can I='create' a='Page'>
        <Button as={Link} to='/pages/new' className='mb-5'>
          <BsPlusLg />{' '}
          {t('addModel', { model: t('models:modelNames.page', { count: 1 }) })}
        </Button>
      </Can>
    </>
  )
}

export default Pages
