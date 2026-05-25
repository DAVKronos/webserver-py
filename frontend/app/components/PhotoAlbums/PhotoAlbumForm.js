import React from 'react'
import FormField from '../Generic/FormField'
import { Form } from 'react-bootstrap'

const photoAlbumFields = [{
  name: 'name_nl',
  type: 'text',
  required: true
}, {
  name: 'name_en',
  type: 'text',
  required: true
}, {
  name: 'is_public',
  type: 'boolean',
  required: true
}, {
  name: 'event_date',
  type: 'date',
  required: true
}, {
  name: 'url',
  type: 'text'
}]

// TODO: make required do something (with react-hook-form)
const PhotoAlbumForm = ({ values, setValue, children }) => {
  return (
    <Form>
      {photoAlbumFields.map((field) => {
        return (
          <FormField
            key={field.name}
            modelName='photoalbum'
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

export default PhotoAlbumForm
