import React from 'react'

// Same sponsor as the old server-rendered footer (templates/react.html).
// The old list with ~15 sponsors was outdated; add new ones here as extra columns.
const Sponsors = () => {
  return (
    <div className='row sponsor-white'>
      <div className='col-6'>
        <a href='https://www.reddropdesign.nl/'>
          <img alt='Red Drop Design' src='/assets/sponsors/sponsor-rdd-cfed8c02ed8aa6b797828abe420f4183eaadc5783ad4c18dd212b203627d19e5.PNG' />
        </a>
      </div>
    </div>
  )
}

export default Sponsors
