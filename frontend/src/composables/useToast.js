import { ref } from 'vue'

const toasts = ref([])
let toastId = 0

export function useToast() {
  function addToast(type, message, duration = 3000) {
    const id = ++toastId
    toasts.value.push({ id, type, message })
    if (duration > 0) {
      setTimeout(() => {
        removeToast(id)
      }, duration)
    }
    return id
  }

  function removeToast(id) {
    const index = toasts.value.findIndex(t => t.id === id)
    if (index > -1) {
      toasts.value.splice(index, 1)
    }
  }

  function success(message, duration) {
    return addToast('success', message, duration)
  }

  function warning(message, duration) {
    return addToast('warning', message, duration)
  }

  function error(message, duration) {
    return addToast('error', message, duration)
  }

  return {
    toasts,
    success,
    warning,
    error,
    removeToast
  }
}
