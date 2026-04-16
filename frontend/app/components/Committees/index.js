import React from 'react'
import { Switch, Route } from 'react-router-dom'
import Committee from './Committee'
import Committees from './Committees'
import EditCommittee from './EditCommittee'
import NewCommittee from './NewCommittee'
import PrivateRoute from '../Generic/PrivateRoute'


const CommitteesRouter = () => {
  return (
    <Switch>
      <Route exact path='/committees' component={Committees} />

      <PrivateRoute
        path='/committees/new'
        component={NewCommittee}
        action='create'
        subject='Committee'
      />

      <PrivateRoute
        path='/committees/:id/edit'
        component={EditCommittee}
        action='update'
        subject='Committee'
      />

      <Route path='/committees/:id' component={Committee} />
    </Switch>
  )
}

export default CommitteesRouter