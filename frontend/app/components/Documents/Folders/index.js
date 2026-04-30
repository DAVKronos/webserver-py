import React from 'react'
import { Switch, Route } from 'react-router-dom'

import FolderView from './FolderView'
import NewFolder from './NewFolder'
import EditFolder from './EditFolder'
import PrivateRoute from '../../Generic/PrivateRoute'

const FolderRouter = () => {
  return (
    <Switch>

      {/* ROOT + SUBFOLDERS VIEW */}
      <Route exact path='/folders/:id?' component={FolderView} />

      {/* CREATE */}
      <PrivateRoute
        path='/folders/new'
        component={NewFolder}
        action='create'
        subject='Folder'
      />

      {/* EDIT */}
      <PrivateRoute
        path='/folders/:id/edit'
        component={EditFolder}
        action='update'
        subject='Folder'
      />

    </Switch>
  )
}

export default FolderRouter