import React from 'react'
import { Container } from 'react-bootstrap'
import Logo from './Logo'
import NavBar from './NavBar'

const Header = () => {
  return (
    <header className='site-header'>
      <div className='site-masthead'>
        <Container fluid='xl' className='site-masthead-inner'>
          <Logo />
          <span className='site-masthead-caption'>DRIENERLOSE ATLETIEK VERENIGING <span aria-hidden='true'>/</span> ENSCHEDE</span>
        </Container>
      </div>
      <div className='site-navigation'>
        <Container fluid='xl'>
          <NavBar />
        </Container>
      </div>
    </header>
  )
}

export default Header
