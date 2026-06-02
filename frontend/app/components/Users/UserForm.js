import React from 'react'
import FormField from '../Generic/FormField'
import { Form } from 'react-bootstrap'
import { useForm, Controller } from 'react-hook-form'
import { getUserTypes } from './queries'

// All fields in a sensible order
const newUserFields = [
  // --- SECTION 1: CORE IDENTIFICATION ---
  {
    name: 'name',
    type: 'text',
    required: true,
    adminOnly: true
  },
  {
    name: 'initials',
    type: 'text',
    required: true,
    adminOnly: true
  },
  {
    name: 'email',
    type: 'text',
    required: true,
    adminOnly: true
  },
  {
    name: 'birthdate',
    type: 'date',
    required: true,
    adminOnly: true
  },
  {
    name: 'sex',
    type: 'text',
    required: true,
    options: ['Male', 'Female', 'Other'],
    adminOnly: false
  }

  // --- SECTION 2: CONTACT & ADDRESS ---
  {
    name: 'phonenumber',
    type: 'text',
    required: true,
    adminOnly: false
  },
  {
    name: 'address',
    type: 'text',
    required: true,
    adminOnly: false
  },
  {
    name: 'postalcode',
    type: 'text',
    required: true,
    adminOnly: false
  },
  {
    name: 'city',
    type: 'text',
    required: true,
    adminOnly: false
  },

  // --- SECTION 3: INSTITUTION & MEMBERSHIP ---
  {
    name: 'institution',
    type: 'text',
    required: true,
    adminOnly: false
  },
  {
    name: 'user_type_id',
    type: 'reference',
    itemQuery: [['user_types'], getUserTypes],
    adminOnly: true
  },
  {
    name: 'joined_in',
    type: 'text',
    required: true,
    adminOnly: false
  },

  // --- SECTION 4: FINANCIAL & ADMINISTRATIVE ---
  {
    name: 'unioncard_number',
    type: 'text',
    required: true,
    adminOnly: true
  },
  {
    name: 'bank_account_number',
    type: 'text',
    required: true,
    adminOnly: true
  }
]

const limitedEditUserFields = [
  {
    name: 'phonenumber',
    type: 'text',
    required: true
  },
  {
    name: 'address',
    type: 'text',
    required: true
  },
  {
    name: 'postalcode',
    type: 'text',
    required: true
  },
  {
    name: 'city',
    type: 'text',
    required: true
  },
  {
    name: 'institution',
    type: 'text',
    required: true
  },
  {
    name: 'sex',
    type: 'text',
    required: true,
    options: ['Male', 'Female', 'Other']
  },
  {
    name: 'joined_in',
    type: 'text'
  },
  {
    name: 'avatar',
    type: 'file'
  }
]

const adminEditUserFields = [
  {
    name: 'name',
    type: 'text',
    required: true
  },
  {
    name: 'initials',
    type: 'text',
    required: true
  },
  {
    name: 'email',
    type: 'text',
    required: true
  },
  {
    name: 'birthdate',
    type: 'date',
    required: true
  },
  {
    name: 'user_type_id',
    type: 'reference',
    itemQuery: [['user_types'], getUserTypes]
  },
  ...limitedEditUserFields, // Add normal user fields
  
  {
    name: 'unioncard_number',
    type: 'text',
    required: true
  },
  {
    name: 'bank_account_number',
    type: 'text',
    required: true
  },
]

// TODO: make required do something (with react-hook-form)
const UserForm = ({ values, setValue, children, fields }) => {
  return (
    <Form>
      {fields.map(
        ({ name, type, required, itemQuery, ...otherProps }) => {
          return (
            <FormField
              {...otherProps}
              key={name}
              modelName='user'
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

export default UserForm
export { limitedEditUserFields, adminEditUserFields, newUserFields }
