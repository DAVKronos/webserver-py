import React from 'react'
import FormField from '../Generic/FormField'
import { Form } from 'react-bootstrap'
import { getFolders } from './queries'

const documentFields = [
  {
    name: 'name',
    type: 'text',
    required: true
  },
  {
    name: 'date',
    type: 'date',
    required: true
  },
  {
    name: 'public',
    type: 'boolean',
    required: true
  },
  {
    name: 'folder_id',
    type: 'reference',
    itemQuery: [['folders'], getFolders]
  },
  {
    name: 'file',
    type: 'file'
  }
]

// TODO: make required do something (with react-hook-form)
const documentForm = ({ values, setValue, children }) => {
  return (
    <Form>
      {documentFields.map(
        ({ name, type, required, itemQuery, ...otherProps }) => {
          return (
            <FormField
              {...otherProps}
              key={name}
              modelName='document'
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

export default documentForm
