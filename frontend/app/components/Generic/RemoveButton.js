import React, { useState } from 'react'
import { Button, Modal } from 'react-bootstrap'
import { useTranslation } from 'react-i18next'

// Remove button with a confirmation pop-up.
// Use it like a normal Button, with onRemove instead of onClick:
//   <RemoveButton size='sm' onRemove={onClickRemove}>{t('remove')}</RemoveButton>
// onRemove only runs after "Remove" is clicked in the pop-up.
const RemoveButton = ({ onRemove, children, variant = 'danger', ...buttonProps }) => {
  const [show, setShow] = useState(false)
  const { t } = useTranslation('generic')

  const close = () => setShow(false)
  const confirm = () => {
    setShow(false)
    onRemove()
  }

  return (
    <>
      <Button variant={variant} {...buttonProps} onClick={() => setShow(true)}>
        {children || t('remove')}
      </Button>

      <Modal show={show} onHide={close}>
        <Modal.Body>{t('confirmRemove')}</Modal.Body>
        <Modal.Footer>
          <Button variant='secondary' onClick={close}>{t('cancel')}</Button>
          <Button variant='danger' onClick={confirm}>{t('remove')}</Button>
        </Modal.Footer>
      </Modal>
    </>
  )
}

export default RemoveButton
