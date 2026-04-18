import { ref, watch } from 'vue'
import { useAnecdoteStore } from '../stores/anecdotes.js'
import { debounce } from '../utils/format.js'

export function useAnecdote() {
  const store = useAnecdoteStore()
  const form = ref({
    class_id: '',
    location: '',
    observation_time: '',
    activity_type: '',
    content: '',
    children_names: [],
    teacher_name: ''
  })

  const recognizedNames = ref([])
  const isRecognizing = ref(false)
  const lastClassId = ref(localStorage.getItem('last_anecdote_class') || '')

  // Initialize form with last class
  if (lastClassId.value) {
    form.value.class_id = lastClassId.value
  }

  // Watch class_id for persistence
  watch(() => form.value.class_id, (val) => {
    if (val) {
      localStorage.setItem('last_anecdote_class', val)
    }
  })

  // Debounced name recognition
  const recognizeNamesDebounced = debounce(async (text) => {
    if (!text || text.length < 5) {
      recognizedNames.value = []
      return
    }
    isRecognizing.value = true
    try {
      const result = await store.recognizeNames(text)
      recognizedNames.value = result?.names || []
    } catch {
      recognizedNames.value = []
    } finally {
      isRecognizing.value = false
    }
  }, 300)

  function addName(name) {
    if (name && !form.value.children_names.includes(name)) {
      form.value.children_names.push(name)
    }
  }

  function removeName(name) {
    form.value.children_names = form.value.children_names.filter(n => n !== name)
  }

  function resetForm() {
    form.value = {
      class_id: lastClassId.value,
      location: '',
      observation_time: '',
      activity_type: '',
      content: '',
      children_names: [],
      teacher_name: ''
    }
    recognizedNames.value = []
  }

  function loadAnecdote(anecdote) {
    form.value = {
      class_id: anecdote.class_id || '',
      location: anecdote.location || '',
      observation_time: anecdote.observation_time || '',
      activity_type: anecdote.activity_type || '',
      content: anecdote.content || '',
      children_names: anecdote.children_names || [],
      teacher_name: anecdote.teacher_name || ''
    }
  }

  async function submitForm(isEdit = false) {
    if (isEdit && store.currentAnecdote?.id) {
      return await store.editAnecdote(store.currentAnecdote.id, form.value)
    }
    return await store.addAnecdote(form.value)
  }

  return {
    form,
    recognizedNames,
    isRecognizing,
    recognizeNamesDebounced,
    addName,
    removeName,
    resetForm,
    loadAnecdote,
    submitForm
  }
}
