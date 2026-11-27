import React from 'react'
import { Container, Row, Col } from 'react-bootstrap'
import { useTranslation } from 'react-i18next'
import { BsBoxArrowUpRight } from 'react-icons/bs'
import logo from '../../images/kronos-logo.svg'
import Contact from './Contact'

// Competition sites, also listed in the nav bar under "Matches"
const externalLinks = [
  { name: 'NSK Kronos', url: 'http://nsk.kronos.nl' },
  { name: 'Campusloop', url: 'http://www.campusloop.nl' },
  { name: 'Johan Knaap Games', url: 'http://jkg.kronos.nl' },
  { name: 'Kronos Beermile', url: 'http://beermile.kronos.nl' }
]

const Footer = () => {
  const { t } = useTranslation('footer')
  const year = new Date().getFullYear()

  return (
    <footer className='site-footer'>
      <div className='site-footer__main'>
        <Container fluid='lg'>
          <Row>
            <Col md={4} className='site-footer__logo'>
              <img src={logo} alt='D.A.V. Kronos' />
            </Col>

            <Col md={4} className='site-footer__col'>
              <h1>{t('contact')}</h1>
              <Contact />
            </Col>

            <Col md={4} className='site-footer__col'>
              <h1>{t('externalLinks')}</h1>
              <ul className='site-footer__links'>
                {externalLinks.map(link => (
                  <li key={link.url}>
                    <BsBoxArrowUpRight aria-hidden='true' />
                    <a href={link.url} target='_blank' rel='noopener noreferrer'>{link.name}</a>
                  </li>
                ))}
              </ul>
            </Col>
          </Row>
        </Container>
      </div>

      <div className='site-footer__bottom'>
        Copyright &copy; {year} - D.A.V. Kronos
      </div>
    </footer>
  )
}

export default Footer
