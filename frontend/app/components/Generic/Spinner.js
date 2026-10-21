import React from 'react'
import kronosLogo from '../../images/logonormal.png'

const DefaultSpinner = ({ inline, size }) => {
  return (
    <div
      className={`kronos-loader${inline ? ' kronos-loader--inline' : ''}${size === 'sm' ? ' kronos-loader--small' : ''}`}
      role='status'
      style={{ margin: !inline && 10 }}
    >
      <span className='kronos-loader__mark' aria-hidden='true'>
        <img src={kronosLogo} alt='' />
      </span>
      <span className='sr-only'>Loading...</span>
    </div>
  )
}

export default DefaultSpinner
