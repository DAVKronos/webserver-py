import React, { useState } from 'react'
import { Nav, Navbar, NavDropdown, Container, Button } from 'react-bootstrap'
import { NavLink } from 'react-router-dom'
import UserMenu from './LoginMenu'
import { useQuery } from 'react-query'
import { getPages } from './queries'
import { useTranslation } from 'react-i18next'
// import LanguageSwitch from './LanguageSwitch' // replaced by LanguageToggle in the user dropdown
import logo from '../../images/kronos-logo-icon.svg'
import MultiLanguageText from "../Generic/MultiLanguageText";

function getPagesForMenu (pages, title) {
  return pages.filter((page) => {
    return page.menu_item === title
  })
}

function getPageLinksForMenu (pages, title) {
  return getPagesForMenu(pages, title).map(page => {
    return <NavDropdown.Item key={page.page_title_nl} as={NavLink} to={`/${page.page_title_nl}`} /* href={`/${page.page_title_nl}`} */>{page.page_title_nl}</NavDropdown.Item>
  })
}

function getHighlightPages (pages) {
  return pages.filter((page) => { 
    return page.is_highlight
  }).map(page => {
    // Highlighted pages as light buttons, on the right next to the user menu
    return (
      <Button key={page.page_title_nl} as={NavLink} to={`/${page.page_title_nl}`} variant='light' className='nav-highlight-btn'>
        <MultiLanguageText nl={page.page_title_nl} en={page.page_title_en} />
      </Button>
    )
  })
}

const NavBar = () => {
  const { isLoading, isError, data } = useQuery('pages', getPages)
  const { t } = useTranslation('navigation')
  const pages = data || []
  return (
    <Navbar id='navbar-kronos' expand='lg' variant='dark' collapseOnSelect>
      <Container>
      <Navbar.Brand as={NavLink} to='/' href='/' exact>
        <img src={logo} alt='' className='navbar-brand-logo' />
        D.A.V. Kronos
      </Navbar.Brand>
      <Navbar.Toggle aria-controls='basic-navbar-nav' />
      <Navbar.Collapse id='basic-navbar-nav' className='flex-wrap'>
        <Nav>
          <NavDropdown title={t('association')} id='basic-nav-dropdown'>
            <NavDropdown.Item as={NavLink} to='/Committees' /* href='/Committees' */>{t('committees')}</NavDropdown.Item>
            {getPageLinksForMenu(pages, 'Vereniging')}
            <NavDropdown.Item as={NavLink} to='/documents' /* href='/documents ' */>{t('documents')}</NavDropdown.Item>
          </NavDropdown>
          <NavDropdown title={t('trainings')} id='basic-nav-dropdown'>
            {getPageLinksForMenu(pages, 'Trainingen')}
          </NavDropdown>
          <NavDropdown title={t('matches')} id='basic-nav-dropdown'>
            <NavDropdown.Item target='_blank' href='http://www.campusloop.nl'>Campusloop</NavDropdown.Item>
            <NavDropdown.Item target='_blank' href='http://jkg.kronos.nl'>Johan Knaap Games</NavDropdown.Item>
            <NavDropdown.Item target='_blank' href='http://nsk.kronos.nl'>NSK Kronos</NavDropdown.Item>
            <NavDropdown.Item target='_blank' href='http://beermile.kronos.nl'>Beermile</NavDropdown.Item>
            {getPageLinksForMenu(pages, 'Wedstrijden')}
          </NavDropdown>
          <Nav.Link as={NavLink} to='/agendaitems' /* href='/agendaitems' */>{t('agenda')}</Nav.Link>
          <Nav.Link as={NavLink} to='/photoalbums' /* href='/photoalbums' */>{t('photos')}</Nav.Link>

        </Nav>
        <Nav className='ml-auto'>
          {getHighlightPages(pages)}
          {/* "Users" link moved to the user dropdown (LoginMenu.js) */}
          <UserMenu />
          {/* <LanguageSwitch /> */}
        </Nav>
      </Navbar.Collapse>
      </Container>
    </Navbar>
  )
}

export default NavBar
