import React from 'react';
import { useQuery } from 'react-query'
import { getUnapprovedNewsItems } from './queries'
import { Table } from 'react-bootstrap'
import { Link } from 'react-router-dom'
import DefaultSpinner from '../Generic/Spinner';

const ApproveNews = () => {
  const { isLoading, isError, data: newsitems, error } = useQuery('unapproved-newsitems', getUnapprovedNewsItems)

  return (
    <>
      <h1>Nieuwsitems goedkeuren</h1>
      <Table striped>
        <thead>
          <tr>
            <th>
              Titel
            </th>
            <th>
              Auteur
            </th>
            <th>
              Laatst gewijzigd op
            </th>
            <th />
          </tr>
        </thead>
        <tbody>
          {isLoading ? <DefaultSpinner /> : newsitems && newsitems.length > 0 ? (
            newsitems.map(newsitem => (
              <tr key={newsitem.id}>
                <td>{newsitem.title}</td>
                <td>{newsitem.user.name}</td>
                <td>{newsitem.updated_at}</td>
                <td><Link to={`/newsitems/${newsitem.id}`}>Bekijken</Link></td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="4" className='text-center'>No newsitems available</td>
            </tr>
          )}
        </tbody>
      </Table>
    </>
  )
}

export default ApproveNews
