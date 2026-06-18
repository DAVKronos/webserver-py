import React from 'react'
import { Switch, Route } from 'react-router-dom'
import { Page, PageWithTag } from './Page'
import PrivateRoute from '../Generic/PrivateRoute'
import EditPage from './EditPage'
import NewPage from './NewPage'

// TODO PageId should be accesed by id or pagetag.
const PagesRouter  = () => {
  return (
    <Switch>
      <PrivateRoute path='/pages/new' component={NewPage} action='create' subject='Page' />
      <PrivateRoute path='/pages/:id/edit' component={EditPage} action='update' subject='Page' />
      <Route path='/pages/:id' component={Page} />
      <Route
        path='/:page_title_nl' render={(routeProps) => {
          // Key is to rerender when switching to a new page
          return <PageWithTag key={routeProps.match.params.page_title_nl} {...routeProps} />
        }}
      />
    </Switch>
  )
}

export default PagesRouter 
