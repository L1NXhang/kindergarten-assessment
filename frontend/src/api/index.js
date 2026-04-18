import axios from 'axios'
import { useToast } from '../composables/useToast.js'

const api = axios.create({
  baseURL: '/api/v1',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Could add loading state here
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    const message = error.response?.data?.message || error.message || '请求失败'
    const toast = useToast()
    if (toast) {
      toast.error(message)
    }
    return Promise.reject(error)
  }
)

export default api
