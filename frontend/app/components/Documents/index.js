import React from 'react'
import { Route, Switch, Redirect } from 'react-router-dom'

import DocumentView from './DocumentView'
import NewDocument from './NewDocument'
import EditDocument from './EditDocument'
import PrivateRoute from '../Generic/PrivateRoute'

const DocumentRouter = () => {
  return (
    <Switch>

      {/* 🚨 NO MORE DOCUMENT LISTING */}
      <Route exact path='/documents'>
        <Redirect to='/folders' />
      </Route>

      {/* CREATE */}
      <PrivateRoute
        path='/documents/new'
        component={NewDocument}
        action='create'
        subject='document'
      />

      {/* EDIT */}
      <PrivateRoute
        path='/documents/:id/edit'
        component={EditDocument}
        action='update'
        subject='document'
      />

      {/* FILE VIEW ONLY */}
      <Route exact path='/documents/:id' component={DocumentView} />

    </Switch>
  )
}

export default DocumentRouter