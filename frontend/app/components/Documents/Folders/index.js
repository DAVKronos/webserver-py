import React from 'react'
import { Switch, Route } from 'react-router-dom'

import FolderView from './FolderView'
import NewFolder from './NewFolder'
import EditFolder from './EditFolder'

const FolderRouter = () => {
  return (
    <Switch>

      <Route exact path='/folders' component={FolderView} />

      <Route exact path='/folders/new' component={NewFolder} />

      <Route exact path='/folders/:id/edit' component={EditFolder} />

      <Route exact path='/folders/:id' component={FolderView} />

    </Switch>
  )
}

export default FolderRouter