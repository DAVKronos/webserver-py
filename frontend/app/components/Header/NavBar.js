import React, { useState } from 'react'
import { Nav, Navbar, NavDropdown } from 'react-bootstrap'
import { NavLink } from 'react-router-dom'
import UserMenu from './LoginMenu'
import { useQuery } from 'react-query'
import { getPages } from './queries'
import { useTranslation } from 'react-i18next'
import { Can } from '../../utils/auth-helper'
import LanguageSwitch from './LanguageSwitch'
import MultiLanguageText from "../Generic/MultiLanguageText";

function getPagesForMenu (pages, title) {
  return pages.filter((page) => {
    return page.menu_item === title
  })
}

function getPageLinksForMenu (pages, title) {
  return getPagesForMenu(pages, title).map(page => {
    return <NavDropdown.Item key={page.page_title_nl} as={NavLink} to={`/${page.page_title_nl}`} href={`/${page.page_title_nl}`}>{page.page_title_nl}</NavDropdown.Item>
  })
}

function getHighlightPages (pages) {
  return pages.filter((page) => { 
    return page.is_highlight
  }).map(page => {
    return <Nav.Link className='highlight' key={page.page_title_nl} as={NavLink} to={`/${page.page_title_nl}`} href={`/${page.page_title_nl}`}><MultiLanguageText nl={page.page_title_nl} en={page.page_title_en} /></Nav.Link>
  })
}

const NavBar = () => {
  const { isLoading, isError, data } = useQuery('pages', getPages)
  const { t } = useTranslation('navigation')
  const pages = data || []
  return (
    <Navbar id='navbar-kronos' expand='lg' variant='dark' collapseOnSelect>
      <Navbar.Brand className='d-md-none d-flex' as={NavLink} to='/' href='/' exact>Kronos</Navbar.Brand>
      <Navbar.Toggle aria-controls='basic-navbar-nav' />
      <Navbar.Collapse id='basic-navbar-nav' className='flex-wrap'>
        <Nav>
          <Nav.Link as={NavLink} to='/' href='/' exact>Home</Nav.Link>
          <NavDropdown title={t('association')} id='basic-nav-dropdown'>
            <NavDropdown.Item as={NavLink} to='/Committees' href='/Committees'>{t('committees')}</NavDropdown.Item>
            {getPageLinksForMenu(pages, 'Vereniging')}
            <NavDropdown.Item as={NavLink} to='/documents' href='/documents '>{t('documents')}</NavDropdown.Item>
          </NavDropdown>
          <NavDropdown title={t('trainings')} id='basic-nav-dropdown'>
            {getPageLinksForMenu(pages, 'Trainingen')}
          </NavDropdown>
          <NavDropdown title={t('matches')} id='basic-nav-dropdown'>
            <NavDropdown.Item target='_blank' href='http://www.campusloop.nl'>Campusloop</NavDropdown.Item>
            <NavDropdown.Item target='_blank' href='http://jkg.kronos.nl'>Johan Knaap Games</NavDropdown.Item>
            <NavDropdown.Item target='_blank' href='http://beermile.kronos.nl'>Beermile</NavDropdown.Item>
            {getPageLinksForMenu(pages, 'Wedstrijden')}
          </NavDropdown>
          <Nav.Link as={NavLink} to='/agendaitems' href='/agendaitems'>{t('agenda')}</Nav.Link>
          <Nav.Link as={NavLink} to='/photoalbums' href='/photoalbums'>{t('photos')}</Nav.Link>

        </Nav>
        <Nav>
          {getHighlightPages(pages)}
        </Nav>
        <Nav className='ml-auto'>

          <Can I='read' an='User'>
            <Nav.Link as={NavLink} to='/users'>{t('users')}</Nav.Link>
          </Can>
          <UserMenu />
          <LanguageSwitch />
        </Nav>
      </Navbar.Collapse>
    </Navbar>
  )
}

export default NavBar
