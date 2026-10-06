import React, { useState } from 'react'
import { Button, Alert } from 'react-bootstrap'
import { useHistory } from 'react-router-dom'
import DefaultSpinner from '../Generic/Spinner'
import { useTranslation } from 'react-i18next'

const NewObjectComponent = ({ FormComponent, createFunction, onSuccess, objectName, ...rest}) => {
  const history = useHistory()

  const [values, setValues] = useState({})
  // const setValue = (fieldName, value) => {
  //   const newValues = { ...values, [fieldName]: value }
  //   setValues(newValues)
  // }
  const setValue = (fieldName, value) => {
    setValues((prevValues) => ({
      ...prevValues,
      [fieldName]: value
    }))
  }
  const [creating, setCreating] = useState(false)
  const [error, setError] = useState(null)

  const cancel = () => {
    history.goBack()
  }


  const { t } = useTranslation('generic')

  const create = () => {
    console.log('State values in NewObjectComponent:', values)

    setCreating(true)
    createFunction({ ...values }).then(result => {
      setCreating(false)
      onSuccess(result)
    }).catch((error) => {
      setCreating(false)
      console.log(error)
      if (error.response.status != 200) {
        if (error.response.data && error.response.data.message) {
          setError(error.response.data.message.join(','))
        } else {
          setError(t('error') + error.response.status)
        }
      }
    })
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
