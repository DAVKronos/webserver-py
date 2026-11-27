import React, { useState } from 'react'
import { Table, Button, Row, Col } from 'react-bootstrap'
import { Link } from 'react-router-dom'
import { useQuery, useQueryCache } from 'react-query'
import { useTranslation } from 'react-i18next'
import { getCommittees, removeCommittee } from './queries'
import MultiLanguageText from '../Generic/MultiLanguageText'
import { Can } from '../../utils/auth-helper'
import DefaultSpinner from '../Generic/Spinner'
import { BsPlusLg } from 'react-icons/bs'
import RemoveButton from '../Generic/RemoveButton'


const CommitteeRow = ({ committee, removeFunction }) => {
  const [removing, setRemoving] = useState(false)

  const onClickRemove = () => {
    setRemoving(true)
    removeFunction(committee.id).then(() => {
      setRemoving(false)
    })
  }

  return (
    <tr key={committee.id}>
      <td>
        <Link to={`/committees/${committee.id}`}>
          <MultiLanguageText
            nl={committee.name_nl}
            en={committee.name_en}
          />
        </Link>
      </td>

      <Can I='update' a='Committee'>
        <td>
          <Button
            variant='warning'
            disabled={removing}
            size='sm'
            as={Link}
            to={`/committees/${committee.id}/edit`}
          >
            Bewerk
          </Button>
        </td>
      </Can>

      <Can I='delete' a='Committee'>
        <td>
          <RemoveButton
            variant='danger'
            disabled={removing}
            size='sm'
            onRemove={onClickRemove}
          >
            {removing ? <DefaultSpinner inline size='sm' /> : 'Verwijder'}
          </RemoveButton>
        </td>
      </Can>
    </tr>
  )
}


function Committees (props) {
  const { isLoading, data } = useQuery(
    'committees',
    getCommittees
  )

  const committees = data
  const { t } = useTranslation('committeePage')
  const queryCache = useQueryCache()

  const removeFunction = (id) => {
    return removeCommittee(id).then(() => {
      queryCache.invalidateQueries(['committees'], { exact: true })
    })
  }

  return (
    <Row>
      <Col md={{ span: 8, offset: 2 }}>
        <div className='kronos-header'>
          <h1>{t('headerText')}</h1>
        </div>

        <div className='page-content'>
          <p className='lead'>{t('pageDescription')}</p>

          <Table striped>
            <thead>
              <tr>
                <th>{t('name')}</th>
                <Can I='update' a='Committee'>
                  <th />
                </Can>
                <Can I='delete' a='Committee'>
                  <th />
                </Can>
              </tr>
            </thead>

            <tbody>
              {committees &&
                committees.map((committee) => {
                  return (
                    <CommitteeRow
                      key={committee.id}
                      committee={committee}
                      removeFunction={removeFunction}
                    />
                  )
                })}
            </tbody>
          </Table>

          {isLoading && <DefaultSpinner />}

          {/* New committee button at the bottom of the content */}
          <Can I='create' a='Committee'>
            <Button as={Link} to='/committees/new'>
              <BsPlusLg />{' '}
              {t('generic:addModel', {
                model: t('models:modelNames.Committee', { count: 1 })
              })}
            </Button>
          </Can>
        </div>
      </Col>
    </Row>
  )
}

export default Committees