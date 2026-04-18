import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import * as childApi from '../api/children.js'

export const useChildStore = defineStore('children', () => {
  const children = ref([])
  const currentChild = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const childCount = computed(() => children.value.length)

  async function fetchChildren(params) {
    loading.value = true
    error.value = null
    try {
      const data = await childApi.getChildren(params)
      children.value = data || []
    } catch (err) {
      error.value = err.message
      children.value = []
    } finally {
      loading.value = false
    }
  }

  async function fetchChildById(id) {
    loading.value = true
    error.value = null
    try {
      const data = await childApi.getChildById(id)
      currentChild.value = data
      return data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function addChild(data) {
    const result = await childApi.createChild(data)
    children.value.push(result)
    return result
  }

  async function editChild(id, data) {
    const result = await childApi.updateChild(id, data)
    const index = children.value.findIndex(c => c.id === id)
    if (index > -1) {
      children.value[index] = result
    }
    if (currentChild.value?.id === id) {
      currentChild.value = result
    }
    return result
  }

  async function removeChild(id) {
    await childApi.deleteChild(id)
    children.value = children.value.filter(c => c.id !== id)
    if (currentChild.value?.id === id) {
      currentChild.value = null
    }
  }

  function clearCurrent() {
    currentChild.value = null
  }

  return {
    children,
    currentChild,
    loading,
    error,
    childCount,
    fetchChildren,
    fetchChildById,
    addChild,
    editChild,
    removeChild,
    clearCurrent
  }
})
