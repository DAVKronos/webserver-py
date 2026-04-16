import { restCall } from '../../utils/rest-helper'


function getCommittee (queryKey, id) {
  return restCall(`committees/${id}`).then((res) => res.data)
}


function getUsersForCommittee (queryKey, id) {
  return getCommittee(queryKey, id).then((committee) => {
    if (committee.memberships) {
      return committee.memberships.map((v) => ({
        id: v.user_id,
        name: v.user.name
      }))
    }
    return []
  })
}


function getCommittees () {
  return restCall('committees').then((res) => res.data)
}


function getCommitteeMemberships (queryKey, committeeId, otherKey) {
  return restCall(`committees/${committeeId}/memberships`).then(
    (res) => res.data
  )
}


function createCommittee (data) {
  return restCall('committees', {
    method: 'POST',
    data: data
  }).then((res) => res.data)
}


function createCommitteeMembership (committeeId, data) {
  return restCall(`committees/${committeeId}/memberships`, {
    method: 'POST',
    data: data
  }).then((res) => res.data)
}


function updateCommittee (id, data) {
  return restCall(`committees/${id}`, {
    method: 'PATCH',
    data: data
  }).then((res) => res.data)
}


function removeCommittee (id) {
  return restCall(`committees/${id}`, { method: 'DELETE' })
}


function removeCommitteeMembership (id, membershipId) {
  return restCall(
    `committees/${id}/memberships/${membershipId}`,
    { method: 'DELETE' }
  )
}


export {
  getCommittee,
  getCommittees,
  getCommitteeMemberships,
  getUsersForCommittee,
  createCommittee,
  updateCommittee,
  removeCommittee,
  createCommitteeMembership,
  removeCommitteeMembership
}