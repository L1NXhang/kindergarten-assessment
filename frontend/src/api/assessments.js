import api from './index.js'

export function getAssessments(params) {
  return api.get('/assessments', { params })
}

export function getAssessmentById(id) {
  return api.get(`/assessments/${id}`)
}

export function createAssessment(data) {
  return api.post('/assessments', data)
}

export function generateAssessment(id) {
  return api.post(`/assessments/${id}/generate`)
}

export function deleteAssessment(id) {
  return api.delete(`/assessments/${id}`)
}

export function getAssessmentReport(id) {
  return api.get(`/assessments/${id}/report`)
}

export function getAssessmentComparison(params) {
  return api.get('/assessments/compare', { params })
}
