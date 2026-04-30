import React from 'react'
import { Route, Switch } from 'react-router-dom'

import documents from './Documents'
import PrivateRoute from '../Generic/PrivateRoute'
import Newdocument from './NewDocument'
import Editdocument from './EditDocument'

const DocumentRouter = () => {
  return (
    <Switch>
      <Route exact path='/documents' component={documents} />

      <PrivateRoute
        path='/documents/new'
        component={Newdocument}
        action='create'
        subject='document'
      />
      <PrivateRoute
        path='/documents/:id/edit'
        component={Editdocument}
        action='update'
        subject='document'
      />
      <Route path='/documents/:folder_id' component={documents} />
    </Switch>
  )
}

export default DocumentRouter
