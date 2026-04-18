<template>
  <div class="sys-page">
    <div class="sys-page-header">
      <h2 class="sys-page-title">系统管理</h2>
      <p class="sys-page-subtitle">管理系统配置、数据备份与统计信息</p>
    </div>

    <div class="sys-grid">
      <!-- Database Backup -->
      <div class="sys-card">
        <div class="sys-card-header">
          <div class="sys-card-icon sys-card-icon--accent">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>
          </div>
          <h3 class="sys-card-title">数据库管理</h3>
        </div>
        <p class="sys-card-desc">备份和恢复系统数据，确保数据安全。</p>
        <div class="sys-card-actions">
          <button class="sys-btn sys-btn--secondary" @click="handleBackup" :disabled="backupLoading">
            <span v-if="backupLoading" class="sys-spinner" style="width:14px;height:14px;border-width:2px;"></span>
            <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
            备份数据
          </button>
          <label class="sys-btn sys-btn--secondary" style="cursor:pointer;">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
            恢复数据
            <input type="file" accept=".db,.sql,.bak" style="display:none" @change="handleRestore" />
          </label>
        </div>
      </div>

      <!-- Teacher Statistics -->
      <div class="sys-card">
        <div class="sys-card-header">
          <div class="sys-card-icon sys-card-icon--warm">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
          </div>
          <h3 class="sys-card-title">教师统计</h3>
        </div>
        <div class="sys-card-body">
          <div v-if="loadingTeachers" class="sys-card-loading">
            <span class="sys-spinner"></span>
          </div>
          <div v-else-if="teachers.length > 0">
            <BaseTable :columns="teacherColumns" :data="teachers" />
          </div>
          <p v-else class="sys-card-empty">暂无教师数据</p>
        </div>
      </div>

      <!-- System Info -->
      <div class="sys-card">
        <div class="sys-card-header">
          <div class="sys-card-icon sys-card-icon--info">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
          </div>
          <h3 class="sys-card-title">系统信息</h3>
        </div>
        <div class="sys-card-body">
          <div class="sys-info-list">
            <div class="sys-info-item">
              <span class="sys-info-label">系统版本</span>
              <span class="sys-info-value">v1.0.0</span>
            </div>
            <div class="sys-info-item">
              <span class="sys-info-label">前端框架</span>
              <span class="sys-info-value">Vue 3 + Vite</span>
            </div>
            <div class="sys-info-item">
              <span class="sys-info-label">UI风格</span>
              <span class="sys-info-value">Linear-style</span>
            </div>
            <div class="sys-info-item">
              <span class="sys-info-label">最后更新</span>
              <span class="sys-info-value">{{ formatDate(new Date()) }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Data Statistics -->
      <div class="sys-card">
        <div class="sys-card-header">
          <div class="sys-card-icon sys-card-icon--data">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 20V10"/><path d="M12 20V4"/><path d="M6 20v-6"/></svg>
          </div>
          <h3 class="sys-card-title">数据统计</h3>
        </div>
        <div class="sys-card-body">
          <div class="sys-info-list">
            <div class="sys-info-item">
              <span class="sys-info-label">班级总数</span>
              <span class="sys-info-value sys-info-value--number">{{ stats.classCount }}</span>
            </div>
            <div class="sys-info-item">
              <span class="sys-info-label">幼儿总数</span>
              <span class="sys-info-value sys-info-value--number">{{ stats.childCount }}</span>
            </div>
            <div class="sys-info-item">
              <span class="sys-info-label">观察记录总数</span>
              <span class="sys-info-value sys-info-value--number">{{ stats.anecdoteCount }}</span>
            </div>
            <div class="sys-info-item">
              <span class="sys-info-label">评估报告总数</span>
              <span class="sys-info-value sys-info-value--number">{{ stats.assessmentCount }}</span>
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
.sys-page {
  max-width: 960px;
  margin: 0 auto;
  padding: 32px 24px;
}

.sys-page-header {
  margin-bottom: 32px;
}

.sys-page-title {
  font-size: 24px;
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0 0 6px 0;
}

.sys-page-subtitle {
  font-size: 14px;
  color: var(--color-text-tertiary);
  margin: 0;
}

.sys-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

@media (max-width: 768px) {
  .sys-grid {
    grid-template-columns: 1fr;
  }

  .sys-page {
    padding: 20px 16px;
  }
}

/* Card */
.sys-card {
  background: #fff;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: 24px;
  transition: box-shadow var(--transition-normal);
}

.sys-card:hover {
  box-shadow: var(--shadow-md);
}

.sys-card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.sys-card-icon {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.sys-card-icon--accent {
  background: var(--color-accent-light);
  color: var(--color-accent);
}

.sys-card-icon--warm {
  background: #FEF3C7;
  color: #D97706;
}

.sys-card-icon--info {
  background: #F0EDE8;
  color: var(--color-text-secondary);
}

.sys-card-icon--data {
  background: #ECFDF5;
  color: #059669;
}

.sys-card-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
}

.sys-card-desc {
  font-size: 13px;
  color: var(--color-text-tertiary);
  margin: 0 0 20px 0;
  line-height: 1.5;
}

.sys-card-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.sys-card-body {
  min-height: 40px;
}

.sys-card-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px 0;
}

.sys-card-empty {
  font-size: 13px;
  color: var(--color-text-tertiary);
  text-align: center;
  padding: 24px 0;
}

/* Buttons */
.sys-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  font-size: 13px;
  font-weight: 500;
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);
  background: #fff;
  color: var(--color-text-primary);
  cursor: pointer;
  transition: all var(--transition-fast);
  line-height: 1.4;
}

.sys-btn:hover:not(:disabled) {
  background: var(--color-border-subtle);
  border-color: var(--color-text-tertiary);
}

.sys-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Info list */
.sys-info-list {
  display: flex;
  flex-direction: column;
}

.sys-info-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid var(--color-border-subtle);
}

.sys-info-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.sys-info-item:first-child {
  padding-top: 0;
}

.sys-info-label {
  font-size: 13px;
  color: var(--color-text-secondary);
}

.sys-info-value {
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text-primary);
}

.sys-info-value--number {
  font-variant-numeric: tabular-nums;
  color: var(--color-accent);
  font-weight: 600;
}

/* Spinner */
.sys-spinner {
  display: inline-block;
  border: 2px solid var(--color-border);
  border-top-color: var(--color-accent);
  border-radius: 50%;
  animation: sys-spin 0.6s linear infinite;
}

@keyframes sys-spin {
  to { transform: rotate(360deg); }
}
</style>
