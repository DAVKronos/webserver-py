import React from 'react'
import { Col, Row, Image, Button } from 'react-bootstrap'
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

  // Helpers for the info block
  const formatDate = (value) => (value ? new Date(value).toLocaleDateString() : '-')
  const formatYear = (value) => (value ? new Date(value).getFullYear() : '-')
  const show = (value) => value || '-'
  // "t.n.v. Hr./Mw." based on gender, nothing for other
  const salutation = (sex) => (sex === 'Male' ? 'Hr. ' : sex === 'Female' ? 'Mw. ' : '')

  return (
    <Row>
      <Col md={{ span: 8, offset: 2 }}>
        <div className='kronos-header user-header'>
          <h1>{user.name}</h1>
          {/* Profile picture: circle, its centre on the bottom edge of the header */}
          <Image src={user.avatar_file?.path || missingAvatar} alt={user.name} roundedCircle className='user-avatar' />
        </div>
        <div className='page-content user-info'>
          {/* General */}
          <Row>
            <Col md={6}>
              <p className='mb-1'>{t('sex')}: <b>{show(user.sex)}</b></p>
              <p>{t('birthdate')}: <b>{formatDate(user.birthdate)}</b></p>
            </Col>
          </Row>

          {/* Contact & address */}
          <Row>
            <Col md={6}>
              <h3>{t('contact')}</h3>
              <p>
                {t('email')}: <b><a href={`mailto:${user.email}`}>{user.email}</a></b><br />
                {t('phone')}: <b>{show(user.phonenumber)}</b>
              </p>
            </Col>
            <Can I='view.extended' this='User'>
              <Col md={6}>
                <h3>{t('address')}</h3>
                <p>
                  {user.address}<br />
                  {user.postalcode}, {user.city}
                </p>
              </Col>
            </Can>
          </Row>

          <hr />

          {/* Membership & study */}
          <Row>
            <Col md={6}>
              <h3>{t('membership')}</h3>
              <p>
                <em>{show(userType)}</em><br />
                {t('kronautSince')} {formatYear(user.created_at)}
                <Can I='view.extended' this='User'>
                  <br />{t('auLicensenumber')}: <b>{show(user.license_number)}</b>
                </Can>
              </p>
            </Col>
            <Col md={6}>
              <h3>{t('study')}</h3>
              <p>
                <em>{show(user.study)}</em><br />
                {t('studentAt')} {show(user.institution)} {t('since')} {show(user.joined_in)}
                <Can I='view.extended' this='User'>
                  <br />{t('studentnumber')}: <b>{show(user.unioncard_number)}</b>
                </Can>
              </p>
            </Col>
          </Row>

          {/* Bank info */}
          <Can I='view.extended' this='User'>
            <h3>{t('bankInfo')}</h3>
            <p>
              IBAN: <b>{show(user.bank_account_number)}</b><br />
              <em>{t('accountHolder')} {salutation(user.sex)}{user.initials}</em>
            </p>
          </Can>

          {/* Committees */}
          <h3>{t('Committees')}</h3>
          {committees && committees.length > 0
            ? (
              <ul>
                {committees.map((c) => (
                  <li key={c.id}>{lang === 'nl' ? c.name_nl : c.name_en}</li>
                ))}
              </ul>
              )
            : <p>-</p>}

          {/* Settings at the bottom of the content */}
          <Can I='edit' this={subject('User', user)}>
            <hr />
            <h6>{t('generic:settings')}</h6>
            <Button variant='warning' as={Link} to={`/users/${user.id}/edit`}>
              {t('generic:edit')}
            </Button>
          </Can>
        </div>
      </Col>
    </Row>
  )
}

export default User
