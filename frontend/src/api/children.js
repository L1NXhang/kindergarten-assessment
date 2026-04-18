import api from './index.js'

export function getChildren(params) {
  return api.get('/children', { params })
}

export function getChildById(id) {
  return api.get(`/children/${id}`)
}

export function createChild(data) {
  return api.post('/children', data)
}

export function updateChild(id, data) {
  return api.put(`/children/${id}`, data)
}

export function deleteChild(id) {
  return api.delete(`/children/${id}`)
}

export function getChildAnecdotes(id, params) {
  return api.get(`/children/${id}/anecdotes`, { params })
}

export function getChildAssessments(id) {
  return api.get(`/children/${id}/assessments`)
}
