import { restCall } from '../../utils/rest-helper'

function getUnapprovedNewsItems () {
  return restCall('newsitems/unapproved').then(res => res.data)
}

export {
  getUnapprovedNewsItems
}
