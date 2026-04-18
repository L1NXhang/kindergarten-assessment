import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router/index.js'
import ToastNotification from './components/common/ToastNotification.vue'
import './styles/base.css'
import './styles/components.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

// Register global toast component
app.component('ToastNotification', ToastNotification)

app.mount('#app')
