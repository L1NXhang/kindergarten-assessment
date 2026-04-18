<template>
  <div class="page-container">
    <div class="page-header">
      <h2>系统管理</h2>
    </div>

    <div class="grid grid-2">
      <!-- Database Backup -->
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">数据库管理</h3>
        </div>
        <div class="system-section">
          <p class="text-sm text-secondary mb-md">备份和恢复系统数据，确保数据安全。</p>
          <div class="flex gap-sm">
            <button class="btn btn-secondary" @click="handleBackup" :disabled="backupLoading">
              <span v-if="backupLoading" class="loading-spinner" style="width:14px;height:14px;border-width:2px;"></span>
              <svg v-else width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
              备份数据
            </button>
            <label class="btn btn-secondary" style="cursor:pointer;">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
              恢复数据
              <input type="file" accept=".db,.sql,.bak" style="display:none" @change="handleRestore" />
            </label>
          </div>
        </div>
      </div>

      <!-- Teacher Statistics -->
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">教师统计</h3>
        </div>
        <div class="system-section">
          <div v-if="loadingTeachers" class="flex-center" style="padding:20px;">
            <span class="loading-spinner"></span>
          </div>
          <div v-else-if="teachers.length > 0">
            <BaseTable :columns="teacherColumns" :data="teachers" />
          </div>
          <p v-else class="text-sm text-tertiary">暂无教师数据</p>
        </div>
      </div>

      <!-- System Info -->
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">系统信息</h3>
        </div>
        <div class="system-section">
          <div class="info-list">
            <div class="info-item">
              <span class="info-label">系统版本</span>
              <span class="info-value">v1.0.0</span>
            </div>
            <div class="info-item">
              <span class="info-label">前端框架</span>
              <span class="info-value">Vue 3 + Vite</span>
            </div>
            <div class="info-item">
              <span class="info-label">UI风格</span>
              <span class="info-value">Linear-style</span>
            </div>
            <div class="info-item">
              <span class="info-label">最后更新</span>
              <span class="info-value">{{ formatDate(new Date()) }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Data Statistics -->
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">数据统计</h3>
        </div>
        <div class="system-section">
          <div class="info-list">
            <div class="info-item">
              <span class="info-label">班级总数</span>
              <span class="info-value">{{ stats.classCount }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">幼儿总数</span>
              <span class="info-value">{{ stats.childCount }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">观察记录总数</span>
              <span class="info-value">{{ stats.anecdoteCount }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">评估报告总数</span>
              <span class="info-value">{{ stats.assessmentCount }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useClassStore } from '../stores/classes.js'
import { useAnecdoteStore } from '../stores/anecdotes.js'
import { useAssessmentStore } from '../stores/assessments.js'
import { useToast } from '../composables/useToast.js'
import BaseTable from '../components/common/BaseTable.vue'
import { formatDate } from '../utils/format.js'

const classStore = useClassStore()
const anecdoteStore = useAnecdoteStore()
const assessmentStore = useAssessmentStore()
const toast = useToast()

const backupLoading = ref(false)
const loadingTeachers = ref(false)
const teachers = ref([])
const stats = reactive({
  classCount: 0,
  childCount: 0,
  anecdoteCount: 0,
  assessmentCount: 0
})

const teacherColumns = [
  { key: 'name', label: '教师' },
  { key: 'anecdote_count', label: '记录数', width: '80px' }
]

onMounted(async () => {
  try {
    await Promise.all([
      classStore.fetchClasses(),
      anecdoteStore.fetchAnecdotes(),
      assessmentStore.fetchAssessments()
    ])
    stats.classCount = classStore.classes.length
    stats.anecdoteCount = anecdoteStore.total
    stats.assessmentCount = assessmentStore.total
  } catch {
    // Silent
  }

  // Load teacher stats
  loadingTeachers.value = true
  try {
    const { default: api } = await import('../api/index.js')
    const result = await api.get('/system/teachers')
    teachers.value = result || []
  } catch {
    teachers.value = []
  } finally {
    loadingTeachers.value = false
  }
})

async function handleBackup() {
  backupLoading.value = true
  try {
    const { default: api } = await import('../api/index.js')
    const blob = await api.get('/system/backup', { responseType: 'blob' })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `backup-${new Date().toISOString().slice(0,10)}.db`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    toast.success('备份成功')
  } catch {
    toast.error('备份失败')
  } finally {
    backupLoading.value = false
  }
}

async function handleRestore(event) {
  const file = event.target.files[0]
  if (!file) return

  try {
    const { default: api } = await import('../api/index.js')
    const formData = new FormData()
    formData.append('file', file)
    await api.post('/system/restore', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    toast.success('恢复成功，请刷新页面')
  } catch {
    toast.error('恢复失败')
  }
}
</script>

<style scoped>
.system-section {
  padding: 4px 0;
}

.info-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.info-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid var(--color-border-subtle);
}

.info-item:last-child {
  border-bottom: none;
}

.info-label {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
}

.info-value {
  font-size: var(--font-size-sm);
  font-weight: 500;
  color: var(--color-text-primary);
}
</style>
