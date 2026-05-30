import React from 'react'
import { Col, Row, Table, Image, Button } from 'react-bootstrap'
import { useTranslation } from 'react-i18next'
import { UserTypeName } from './UserType'
import { useQuery } from 'react-query'
import { Can } from '../../utils/auth-helper'
import { getUserCommittees, getUser } from './queries'
import { subject } from '@casl/ability'

import { Link, useHistory } from 'react-router-dom'
import missingAvatar from '../../images/avatar-missing.png'

import './User.scss'

const User = (props) => {
  const id = parseInt(props.match.params.id)
  const { isLoadingUser, data: user } = useQuery(['users', id], getUser)
  const { isLoadingCommittees, data: committees } = useQuery(['users', id, 'committees'], getUserCommittees)
  const { t, i18n } = useTranslation('userpage')
  const lang = i18n.language
  if (!user) return null
  const date = new Date(user.birthdate)
  const created_at = new Date(user.created_at)
  const userType = i18n.language === 'nl' ? user.user_type && user.user_type.name_nl : user.user_type && user.user_type.name_en

  return (
    <>
      <h1>{user.name}</h1>
      <Row>
        <Col>
          <Table>
            <tbody>
              <tr>
                <td>
                  <b>{t('initials')}</b>
                </td>
                <td>{user.initials}</td>
              </tr>
              <tr>
                <td>
                  <b>{t('birthdate')}</b>
                </td>
                <td>{date.toLocaleDateString()}</td>
              </tr>
              <tr>
                <td>
                  <b>E-mail</b>
                </td>
                <td>{user.email}</td>
              </tr>
              <tr>
                <td>
                  <b>{t('membertype')}</b>
                </td>
                <td>{userType}</td>
              </tr>
              <tr>
                <td>
                  <b>{t('phonenumber')}</b>
                </td>
                <td>{user.phonenumber}</td>
              </tr>
              {user.institution && <tr>
                <td>
                  <b>{t('institution')}</b>
                </td>
                <td>{user.institution}</td>
              </tr>}
              {user.joined_in && <tr>
                <td>
                  <b>{t('memberSince')}</b>
                </td>
                <td>{user.joined_in}</td>
              </tr>}
              <tr>
                <td>
                  <b>{t('sex')}</b>
                </td>
                <td>{user.sex}</td>
              </tr>
              
              <Can I='view.extended' this='User'>
                <tr>
                  <td>
                    <b>{t('address')}</b>
                  </td>
                  <td>{user.address}</td>
                </tr>
                <tr>
                  <td>
                    <b>{t('postalcode')}</b>
                  </td>
                  <td>{user.postalcode}</td>
                </tr>
                <tr>
                  <td>
                    <b>{t('city')}</b>
                  </td>
                  <td>{user.city}</td>
                </tr>
                <tr>
                  <td>
                    <b>{t('unioncardnumber')}</b>
                  </td>
                  <td>{user.unioncard_number}</td>
                </tr>
                <tr>
                  <td>
                    <b>{t('banknumber')}</b>
                  </td>
                  <td>{user.bank_account_number}</td>
                </tr>
                <tr>
                  <td>
                    <b>{t('createdat')}</b>
                  </td>
                  <td>{created_at.toLocaleDateString()}</td>
                </tr>
              </Can>
              <tr>
                <td>
                  <b>{t('Committees')}</b>
                </td>
                <td>
                  {committees?.map((c) => (lang === 'nl' ? c.name_nl : c.name_en)).toString()}
                </td>
              </tr>
            </tbody>
          </Table>
        </Col>
        <Col>
          <section className='polaroid'>
            <figure>
              {user.avatar_file && <Image src={user.avatar_file?.path}/>}
              {!user.avatar_file && <Image src={missingAvatar}/>}
              <figcaption>{user.name}</figcaption>
            </figure>
          </section>
        </Col>
      </Row>
      <Row>
        <Col>
          <Can I='edit' this={subject('User', user)}>
            <Button as={Link} to={`/users/${user.id}/edit`}>
              {t('generic:edit')}
            </Button>
          </Can>
          {/* <Can I='editpassword' this={subject('User', user)}>
            <Button as={Link} to={`/users/${user.id}/password/edit`}>
              {t('changePassword')}
            </Button>
          </Can> */}
        </Col>
      </Row>
    </>
  )
  return null
}

export default User
