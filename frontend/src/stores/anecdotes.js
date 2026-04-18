import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as anecdoteApi from '../api/anecdotes.js'

export const useAnecdoteStore = defineStore('anecdotes', () => {
  const anecdotes = ref([])
  const currentAnecdote = ref(null)
  const total = ref(0)
  const loading = ref(false)
  const error = ref(null)

  async function fetchAnecdotes(params) {
    loading.value = true
    error.value = null
    try {
      const data = await anecdoteApi.getAnecdotes(params)
      anecdotes.value = data?.items || data || []
      total.value = data?.total || anecdotes.value.length
    } catch (err) {
      error.value = err.message
      anecdotes.value = []
    } finally {
      loading.value = false
    }
  }

  async function fetchAnecdoteById(id) {
    loading.value = true
    error.value = null
    try {
      const data = await anecdoteApi.getAnecdoteById(id)
      currentAnecdote.value = data
      return data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function addAnecdote(data) {
    const result = await anecdoteApi.createAnecdote(data)
    anecdotes.value.unshift(result)
    total.value++
    return result
  }

  async function editAnecdote(id, data) {
    const result = await anecdoteApi.updateAnecdote(id, data)
    const index = anecdotes.value.findIndex(a => a.id === id)
    if (index > -1) {
      anecdotes.value[index] = result
    }
    if (currentAnecdote.value?.id === id) {
      currentAnecdote.value = result
    }
    return result
  }

  async function removeAnecdote(id) {
    await anecdoteApi.deleteAnecdote(id)
    anecdotes.value = anecdotes.value.filter(a => a.id !== id)
    total.value--
    if (currentAnecdote.value?.id === id) {
      currentAnecdote.value = null
    }
  }

  async function recognizeNames(text) {
    return await anecdoteApi.recognizeNames(text)
  }

  function clearCurrent() {
    currentAnecdote.value = null
  }

  return {
    anecdotes,
    currentAnecdote,
    total,
    loading,
    error,
    fetchAnecdotes,
    fetchAnecdoteById,
    addAnecdote,
    editAnecdote,
    removeAnecdote,
    recognizeNames,
    clearCurrent
  }
})
