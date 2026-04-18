import api from './index.js'

export function exportReport(id, format = 'pdf') {
  return api.get(`/reports/export/${id}`, {
    params: { format },
    responseType: 'blob'
  })
}

export function exportClassReport(classId, params) {
  return api.get(`/reports/class/${classId}/export`, {
    params,
    responseType: 'blob'
  })
}

export function exportChildReport(childId, params) {
  return api.get(`/reports/child/${childId}/export`, {
    params,
    responseType: 'blob'
  })
}

export function getDashboardStats() {
  return api.get('/reports/dashboard')
}
