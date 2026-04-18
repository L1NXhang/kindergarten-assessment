import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as assessmentApi from '../api/assessments.js'

export const useAssessmentStore = defineStore('assessments', () => {
  const assessments = ref([])
  const currentAssessment = ref(null)
  const total = ref(0)
  const loading = ref(false)
  const error = ref(null)

  async function fetchAssessments(params) {
    loading.value = true
    error.value = null
    try {
      const data = await assessmentApi.getAssessments(params)
      assessments.value = data?.items || data || []
      total.value = data?.total || assessments.value.length
    } catch (err) {
      error.value = err.message
      assessments.value = []
    } finally {
      loading.value = false
    }
  }

  async function fetchAssessmentById(id) {
    loading.value = true
    error.value = null
    try {
      const data = await assessmentApi.getAssessmentById(id)
      currentAssessment.value = data
      return data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function addAssessment(data) {
    const result = await assessmentApi.createAssessment(data)
    assessments.value.unshift(result)
    total.value++
    return result
  }

  async function generateAssessmentReport(id) {
    const result = await assessmentApi.generateAssessment(id)
    const index = assessments.value.findIndex(a => a.id === id)
    if (index > -1) {
      assessments.value[index] = result
    }
    if (currentAssessment.value?.id === id) {
      currentAssessment.value = result
    }
    return result
  }

  async function removeAssessment(id) {
    await assessmentApi.deleteAssessment(id)
    assessments.value = assessments.value.filter(a => a.id !== id)
    total.value--
    if (currentAssessment.value?.id === id) {
      currentAssessment.value = null
    }
  }

  async function fetchComparison(params) {
    return await assessmentApi.getAssessmentComparison(params)
  }

  function clearCurrent() {
    currentAssessment.value = null
  }

  return {
    assessments,
    currentAssessment,
    total,
    loading,
    error,
    fetchAssessments,
    fetchAssessmentById,
    addAssessment,
    generateAssessmentReport,
    removeAssessment,
    fetchComparison,
    clearCurrent
  }
})
