import React, { useState } from 'react'
import { Button, Alert, Row, Col } from 'react-bootstrap'
import { useHistory } from 'react-router-dom'
import DefaultSpinner from '../Generic/Spinner'
import AdminCard from './AdminCard'
import { useTranslation } from 'react-i18next'

// pageLayout: kronos-header + white content container in the centre column, Create/Cancel in a card on the side.
// Without it the page looks as before (used by all other "new" pages).
const NewObjectComponent = ({ FormComponent, createFunction, onSuccess, objectName, pageLayout = false, ...rest }) => {
  const history = useHistory()

  const [values, setValues] = useState({})
  const setValue = (fieldName, value) => {
    const newValues = { ...values, [fieldName]: value }
    setValues(newValues)
  }
  const [creating, setCreating] = useState(false)
  const [error, setError] = useState(null)

  const cancel = () => {
    history.goBack()
  }

  const create = () => {
    setCreating(true)
    createFunction({ ...values }).then(result => {
      setCreating(false)
      onSuccess(result)
    }).catch((error) => {
      setCreating(false)
      console.log(error)
      if (error.response.status === 400) {
        if (error.response.data && error.response.data.message) {
          setError(error.response.data.message.join(','))
        } else {
          setError('Sommige velden missen')
        }
      }
    })
  }

  const { t } = useTranslation('generic')
  const title = t('addModel', { model: t(`models:modelNames.${objectName}`) })

  if (pageLayout) {
    return (
      <Row>
        <Col md={{ span: 8, offset: 2 }}>
          <div className='kronos-header'>
            <h1>{title}</h1>
          </div>
          <div className='page-content'>
            {error && <Alert variant='danger'><p>{error}</p></Alert>}
            <FormComponent values={values} setValue={setValue} {...rest} />
          </div>
        </Col>
        <Col md={2}>
          <AdminCard>
            <Button block onClick={() => create()} disabled={creating}>
              {creating && <DefaultSpinner inline size='sm' />}
              {!creating && t('create')}
            </Button>
            <Button block variant='secondary' onClick={() => cancel()}>{t('cancel')}</Button>
          </AdminCard>
        </Col>
      </Row>
    )
  }

  return (
    <>
      <h1>{t('addModel', { model: t(`models:modelNames.${objectName}`) })}</h1>
      {error && <Alert variant='danger'><p>{error}</p></Alert>}
      <FormComponent 
      values={values} 
      setValue={setValue}
      {...rest}
      />
      <Button onClick={() => create()}>
        {creating && <DefaultSpinner inline size='sm' />}
        {!creating && t('create')}
      </Button>
      <Button variant='secondary' onClick={() => cancel()}>{t('cancel')}</Button>
    </>
  )
}

export default NewObjectComponent
