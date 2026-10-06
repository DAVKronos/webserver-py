import React from 'react'
import FormField from '../Generic/FormField'
import { Form } from 'react-bootstrap'

const pageFields = [{
  name: 'page_title_nl',
  type: 'text',
  required: true
}, {
  name: 'page_title_en',
  type: 'text',
  required: true
},
{
  name: 'is_highlight',
  type: 'boolean'
},
{
  name: 'is_public',
  type: 'boolean'
}, {
  name: 'menu_item',
  type: 'text'
},
{
  name: 'sort_order',
  type: 'number'
},
{
  name: 'content_nl',
  type: 'textarea',
  required: true
}, {
  name: 'content_en',
  type: 'textarea',
  required: true
}]

// TODO: make required do something (with react-hook-form)
const PageForm = ({ values, setValue, children }) => {
  return (
    <Form>
      {pageFields.map((field) => {
        return (
          <FormField
            key={field.name}
            modelName='page'
            fieldName={field.name}
            value={values[field.name]}
            setValue={(v) => setValue(field.name, v)}
            type={field.type}
            required={field.required}
          />
        )
      })}
      {children}
    </Form>
  )
}

export default PageForm
