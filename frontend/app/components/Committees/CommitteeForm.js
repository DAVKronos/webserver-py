import React from 'react'
import FormField from '../Generic/FormField'
import { Form } from 'react-bootstrap'
import { getUsers } from '../Users/queries'


const committeeFields = [
  {
    name: 'name_nl',
    type: 'text',
    required: true
  },
  {
    name: 'name_en',
    type: 'text',
    required: true
  },
  {
    name: 'description_nl',
    type: 'textarea',
    required: true
  },
  {
    name: 'description_en',
    type: 'textarea',
    required: true
  }
]


// TODO: make required do something (with react-hook-form)
const CommitteeForm = ({ values, setValue, children }) => {
  return (
    <Form>
      {committeeFields.map(
        ({ name, type, required, itemQuery, ...otherProps }) => {
          return (
            <FormField
              {...otherProps}
              key={name}
              modelName='committee'
              fieldName={name}
              value={values[name]}
              setValue={(v) => setValue(name, v)}
              type={type}
              required={required}
              itemQuery={itemQuery}
            />
          )
        }
      )}
      {children}
    </Form>
  )
}

export default CommitteeForm