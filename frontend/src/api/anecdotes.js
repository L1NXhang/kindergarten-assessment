import api from './index.js'

export function getAnecdotes(params) {
  return api.get('/anecdotes', { params })
}

export function getAnecdoteById(id) {
  return api.get(`/anecdotes/${id}`)
}

export function createAnecdote(data) {
  return api.post('/anecdotes', data)
}

export function updateAnecdote(id, data) {
  return api.put(`/anecdotes/${id}`, data)
}

export function deleteAnecdote(id) {
  return api.delete(`/anecdotes/${id}`)
}

export function recognizeNames(text) {
  return api.post('/anecdotes/recognize-names', { text })
}
