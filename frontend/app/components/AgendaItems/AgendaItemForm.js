import { useQuery } from 'react-query'
import { getAgendaitemTypes, getCommittees } from './queries'
import React, { useContext } from 'react'
import FormField from '../Generic/FormField'
import { authContext } from '../../utils/AuthContext'
import { Form } from 'react-bootstrap'

const agendaItemFields = [{
  name: 'name_nl',
  type: 'text',
  required: true
}, {
  name: 'name_en',
  type: 'text',
  required: true
}, {
  name: 'agendaitem_type_id',
  type: 'reference',
  required: true,
  itemQuery: [['agendaitemtypes'], getAgendaitemTypes]
}, {
  name: 'date',
  type: 'datetime',
  required: true
}, {
  name: 'is_internal',
  type: 'boolean'
}, {
  name: 'description_nl',
  type: 'textarea'
}, {
  name: 'description_en',
  type: 'textarea'
}, {
  name: 'location',
  type: 'text'
}, {
  name: 'url',
  type: 'text'
}, {
  name: 'committee_id',
  type: 'reference',
  itemQuery: userId => [['committees'], getCommittees, { enabled: userId }]
}, {
  name: 'can_subscribe',
  type: 'boolean'
}, {
  name: 'subscription_deadline',
  type: 'datetime',
  conditionField: 'can_subscribe'
}, {
  name: 'max_subscription',
  type: 'number',
  conditionField: 'can_subscribe'
}]

// TODO: make required do something (with react-hook-form)
const AgendaItemForm = ({ values, setValue, children }) => {
  const { user } = useContext(authContext)
  const userId = user && user.id
  return (
    <Form>
      {agendaItemFields.map(({ name, type, required, itemQuery, conditionField, ...otherProps }) => {
        const newItemQuery = name === 'committee_id' ? itemQuery(userId) : itemQuery
        if (!conditionField || values[conditionField]) {
          return (
            <FormField
              {...otherProps}
              key={name}
              modelName='agendaitem'
              fieldName={name}
              value={values[name]}
              setValue={(v) => setValue(name, v)}
              type={type}
              required={required}
              itemQuery={newItemQuery}
            />
          )
        }
      })}
      {children}
    </Form>
  )
}

export default AgendaItemForm
