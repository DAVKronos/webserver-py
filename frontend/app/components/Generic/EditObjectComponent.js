import React, { useState, useEffect } from 'react'
import { Alert, Button, Row, Col } from 'react-bootstrap'
import { useHistory } from 'react-router-dom'
import DefaultSpinner from '../Generic/Spinner'
import AdminCard from './AdminCard'
import { useTranslation } from 'react-i18next'

// pageLayout: kronos-header + white content container in the centre column, Save/Cancel in a card on the side.
// Without it the edit page looks as before (used by all other edit pages).
const EditObjectComponent = ({ objectName, id, existingObject, updateFunction, FormComponent, onSuccess, pageLayout = false, ...rest }) => {
  const history = useHistory()

  const [values, setValues] = useState({ ...existingObject })

  // ✅ FIX: sync wanneer existingObject later binnenkomt
  useEffect(() => {
    if (existingObject) {
      setValues({ ...existingObject })
    }
  }, [existingObject])

  const setValue = (fieldName, value) => {
    const newValues = { ...values, [fieldName]: value }
    setValues(newValues)
  }

  const [saving, setSaved] = useState(false)
  const [message, setMessage] = useState('')

  const cancel = () => {
    history.goBack()
  }

  const update = () => {
    setSaved(true)
    updateFunction(id, { ...values }).then(result => {
      setSaved(false)
      setMessage('Agenda item updated!')
      onSuccess(result)
    }).catch(() => {
      setSaved(false)
    })
  }

  const { t } = useTranslation('generic')
  const title = t('editModel', { model: t(`models:modelNames.${objectName}`, { count: 1 }) })

  if (pageLayout) {
    return (
      <Row>
        <Col md={{ span: 8, offset: 2 }}>
          {message && <Alert variant='success' dismissible onClose={() => setMessage('')}>{message}</Alert>}
          <div className='kronos-header'>
            <h1>{title}</h1>
          </div>
          <div className='page-content'>
            <FormComponent values={values} setValue={setValue} />
          </div>
        </Col>
        <Col md={2}>
          <AdminCard>
            <Button block onClick={() => update()} disabled={saving}>
              {saving && <DefaultSpinner inline size='sm' />}
              {!saving && t('save')}
            </Button>
            <Button block variant='secondary' onClick={() => cancel()}>{t('cancel')}</Button>
          </AdminCard>
        </Col>
      </Row>
    )
  }

  return (
    <>
      {message && <Alert variant='success' dismissible onClose={() => setMessage('')}>{message}</Alert>}
      <h1>{t('editModel', { model: t(`models:modelNames.${objectName}`, { count: 1 }) })}</h1>
      <FormComponent
        values={values}
        setValue={setValue}
        
        
      >
        <Button onClick={() => update()} disabled={saving}>
          {saving && <DefaultSpinner inline size='sm' />}
          {!saving && t('save')}
        </Button>
        <Button variant='secondary' onClick={() => cancel()}>{t('cancel')}</Button>
      </FormComponent>
    </>
  )
}

export default EditObjectComponent
