import api from './index.js'

export function getClasses() {
  return api.get('/classes')
}

export function getClassById(id) {
  return api.get(`/classes/${id}`)
}

export function createClass(data) {
  return api.post('/classes', data)
}

export function updateClass(id, data) {
  return api.put(`/classes/${id}`, data)
}

export function deleteClass(id) {
  return api.delete(`/classes/${id}`)
}

export function importClassExcel(file) {
  const formData = new FormData()
  formData.append('file', file)
  return api.post('/classes/import', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}

export function getClassChildren(id) {
  return api.get(`/classes/${id}/children`)
}

export function getClassStats(id) {
  return api.get(`/classes/${id}/stats`)
}
