import React from 'react'
import logowide from '../../images/logowide.png'
import { Link } from 'react-router-dom'

const Logo = () => {
  return (
    <div className='logo-container'>
      <Link className='brand-link' to='/' aria-label='Kronos home'>
        <img className='brand-logo' src={logowide} alt='Drienerlose Atletiek Vereniging Kronos' />
      </Link>
    </div>
  )
}

export default Logo
