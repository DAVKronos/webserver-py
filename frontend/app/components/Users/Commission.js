import React, { Component } from 'react'
import { ListGroup } from 'react-bootstrap'
import { useQuery } from 'react-query'
import { useTranslation } from 'react-i18next'
import { getMemberships } from './queries'

class RegularText extends Component {
  state = {
    text: this.props.text
  }

  render () {
    return this.state.text
  }
}

const MembershipList = ({ user }) => {
  const { t, i18n } = useTranslation('generic')
  const lang = i18n.language
  const { isLoading, isError, data, error } = useQuery(['memberships', user.id], getMemberships)
  const Committees = data
  return (
    <>
      {Committees && Committees.map(Committee => {
        return <RegularText key={Committee.id} text={Committee.name} />
      })}
    </>
  )
}

export { MembershipList }
