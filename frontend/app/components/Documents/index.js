import React from 'react'
import { Route, Switch } from 'react-router-dom'

import DocumentsPage from './Documents'
import DocumentView from './DocumentView'
import NewDocument from './NewDocument'
import EditDocument from './EditDocument'
import PrivateRoute from '../Generic/PrivateRoute'

const DocumentRouter = () => {
  return (
    <Switch>

      {/* ALL DOCUMENTS OR FOLDER VIEW */}
      <Route exact path='/documents' component={DocumentsPage} />

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

      {/* 🔥 THIS IS THE FIX: SINGLE FILE VIEW */}
      <Route exact path='/documents/:id' component={DocumentView} />

    </Switch>
  )
}

export default DocumentRouter