import React from 'react'
import { useQuery, useQueryCache } from 'react-query'
import DefaultSpinner from '../Generic/Spinner'
import { useHistory } from 'react-router-dom'
import EditObjectComponent from '../Generic/EditObjectComponent'
import { getPage, updatePage } from './queries'
import PageForm from './PageForm'

const EditPageWithData = (props) => {
  const id = parseInt(props.match.params.id)
  const { isLoading, isError, data, error } = useQuery(['pages', id], getPage)
  if (isLoading) {
    return <DefaultSpinner />
  }
  return data && <EditPage page={data} />
}

const EditPage = ({ page }) => {
  const queryCache = useQueryCache()
  const history = useHistory()
  const { id, page_title_nl, page_title_en, menu_item, is_highlight, sort_order, content_nl, content_en } = page

  const editableFields = { page_title_nl, page_title_en, menu_item, is_highlight, is_public: page.is_public, sort_order, content_nl, content_en }
  const onSuccess = (savedPage) => {
    queryCache.setQueryData(['pages', savedPage.id], savedPage)
    queryCache.invalidateQueries(['pages'], { exact: true })

    history.push(`/pages/${savedPage.id}`)
  }

  return (
    <EditObjectComponent
      id={id}
      existingObject={editableFields}
      objectName='page'
      updateFunction={updatePage}
      onSuccess={onSuccess}
      FormComponent={PageForm}
    />
  )
}

export default EditPageWithData
