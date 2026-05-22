import React from 'react'
import { Switch, Route } from 'react-router-dom'
import ClubRecords from './ClubRecords'

const ClubRecordsRouter = () => {
  return (
    <Switch>
      <Route exact path='/ClubRecords' component={ClubRecords} />
    </Switch>
  )
}

export default ClubRecordsRouter
