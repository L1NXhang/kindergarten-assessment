import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import * as classApi from '../api/classes.js'

export const useClassStore = defineStore('classes', () => {
  const classes = ref([])
  const currentClass = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const classCount = computed(() => classes.value.length)

  async function fetchClasses() {
    loading.value = true
    error.value = null
    try {
      const data = await classApi.getClasses()
      classes.value = data || []
    } catch (err) {
      error.value = err.message
      classes.value = []
    } finally {
      loading.value = false
    }
  }

  async function fetchClassById(id) {
    loading.value = true
    error.value = null
    try {
      const data = await classApi.getClassById(id)
      currentClass.value = data
      return data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function addClass(data) {
    const result = await classApi.createClass(data)
    classes.value.push(result)
    return result
  }

  async function editClass(id, data) {
    const result = await classApi.updateClass(id, data)
    const index = classes.value.findIndex(c => c.id === id)
    if (index > -1) {
      classes.value[index] = result
    }
    if (currentClass.value?.id === id) {
      currentClass.value = result
    }
    return result
  }

  async function removeClass(id) {
    await classApi.deleteClass(id)
    classes.value = classes.value.filter(c => c.id !== id)
    if (currentClass.value?.id === id) {
      currentClass.value = null
    }
  }

  async function importExcel(file) {
    const result = await classApi.importClassExcel(file)
    await fetchClasses()
    return result
  }

  function clearCurrent() {
    currentClass.value = null
  }

  return {
    classes,
    currentClass,
    loading,
    error,
    classCount,
    fetchClasses,
    fetchClassById,
    addClass,
    editClass,
    removeClass,
    importExcel,
    clearCurrent
  }
})
