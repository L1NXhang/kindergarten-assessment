<template>
  <div class="assessment-list-page">
    <!-- Page Header -->
    <div class="page-header">
      <div class="page-header-left">
        <h2 class="page-title">阶段性评估</h2>
        <p class="page-subtitle">管理和查看所有评估记录</p>
      </div>
      <button class="btn-primary" @click="showNewModal = true">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
        新建评估
      </button>
    </div>

    <!-- Filter Bar -->
    <div class="filter-bar">
      <div class="filter-group">
        <svg class="filter-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>
        <select v-model="filters.status" class="filter-select" @change="handleFilter">
          <option value="">全部状态</option>
          <option v-for="(info, key) in ASSESSMENT_STATUS" :key="key" :value="key">{{ info.label }}</option>
        </select>
      </div>
      <div class="filter-group">
        <svg class="filter-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
        <select v-model="filters.class_id" class="filter-select" @change="handleFilter">
          <option value="">全部班级</option>
          <option v-for="cls in classes" :key="cls.id" :value="cls.id">{{ cls.name }}</option>
        </select>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <span class="loading-text">加载评估列表...</span>
    </div>

    <!-- Assessment Grid -->
    <div v-else-if="assessments.length > 0" class="assessment-grid">
      <AssessmentCard
        v-for="item in assessments"
        :key="item.id"
        :assessment="item"
        @click="$router.push(`/assessments/${item.id}`)"
      />
    </div>

    <!-- Empty State -->
    <div v-else class="empty-state">
      <div class="empty-state-icon">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
      </div>
      <h3 class="empty-state-title">暂无评估记录</h3>
      <p class="empty-state-desc">创建新的评估来生成幼儿发展报告</p>
      <button class="btn-primary" @click="showNewModal = true">新建评估</button>
    </div>

    <!-- New Assessment Modal -->
    <BaseModal v-model="showNewModal" title="新建评估">
      <div class="modal-form">
        <div class="form-field">
          <label class="form-label">评估类型</label>
          <select v-model="newForm.type" class="form-select">
            <option value="class">班级评估</option>
            <option value="personal">个人评估</option>
          </select>
        </div>
        <div class="form-field">
          <label class="form-label">{{ newForm.type === 'class' ? '选择班级' : '选择幼儿' }}</label>
          <select v-model="newForm.target_id" class="form-select">
            <option value="">请选择</option>
            <option v-if="newForm.type === 'class'" v-for="cls in classes" :key="cls.id" :value="cls.id">{{ cls.name }}</option>
          </select>
        </div>
        <div class="form-field">
          <label class="form-label">评估周期</label>
          <input type="text" v-model="newForm.period" class="form-input" placeholder="例如：2024年上学期" />
        </div>
      </div>
      <template #footer>
        <div class="modal-footer">
          <button class="btn-secondary" @click="showNewModal = false">取消</button>
          <button class="btn-primary" @click="handleCreate" :disabled="!newForm.target_id">创建并生成</button>
        </div>
      </template>
    </BaseModal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useAssessmentStore } from '../stores/assessments.js'
import { useClassStore } from '../stores/classes.js'
import { useToast } from '../composables/useToast.js'
import AssessmentCard from '../components/assessment/AssessmentCard.vue'
import EmptyState from '../components/common/EmptyState.vue'
import BaseModal from '../components/common/BaseModal.vue'
import { ASSESSMENT_STATUS } from '../utils/constants.js'

const assessmentStore = useAssessmentStore()
const classStore = useClassStore()
const toast = useToast()

const loading = ref(false)
const assessments = ref([])
const classes = ref([])
const showNewModal = ref(false)

const filters = reactive({
  status: '',
  class_id: ''
})

const newForm = reactive({
  type: 'class',
  target_id: '',
  period: ''
})

onMounted(async () => {
  loading.value = true
  try {
    await Promise.all([
      classStore.fetchClasses(),
      assessmentStore.fetchAssessments()
    ])
    classes.value = classStore.classes
    assessments.value = assessmentStore.assessments
  } catch {
    toast.error('加载失败')
  } finally {
    loading.value = false
  }
})

function handleFilter() {
  loading.value = true
  assessmentStore.fetchAssessments({ ...filters }).then(() => {
    assessments.value = assessmentStore.assessments
  }).finally(() => {
    loading.value = false
  })
}

async function handleCreate() {
  if (!newForm.target_id) return
  try {
    const data = {
      type: newForm.type,
      period: newForm.period
    }
    if (newForm.type === 'class') {
      data.class_id = newForm.target_id
    } else {
      data.child_id = newForm.target_id
    }
    const assessment = await assessmentStore.addAssessment(data)
    showNewModal.value = false
    toast.success('评估已创建')
    // Navigate to detail
    // Use router
    const { useRouter } = await import('vue-router')
    const router = useRouter()
    router.push(`/assessments/${assessment.id}`)
  } catch {
    // Error handled by interceptor
  }
}
</script>

<style scoped>
.assessment-list-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 24px;
}

/* Page Header */
.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 28px;
}

.page-title {
  font-size: 22px;
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0 0 4px 0;
  letter-spacing: -0.02em;
}

.page-subtitle {
  font-size: 14px;
  color: var(--color-text-tertiary);
  margin: 0;
}

/* Buttons */
.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 10px 20px;
  background: var(--color-accent);
  color: #fff;
  border: none;
  border-radius: var(--radius-md);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.btn-primary:hover {
  background: #4338CA;
  box-shadow: var(--shadow-sm);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 10px 20px;
  background: #fff;
  color: var(--color-text-secondary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.btn-secondary:hover {
  background: var(--color-accent-light);
  color: var(--color-accent);
  border-color: var(--color-accent-subtle);
}

/* Filter Bar */
.filter-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 24px;
  padding: 12px 16px;
  background: #fff;
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--radius-lg);
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-icon {
  color: var(--color-text-tertiary);
  flex-shrink: 0;
}

.filter-select {
  padding: 7px 32px 7px 12px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  font-size: 13px;
  color: var(--color-text-primary);
  background: #fff url("data:image/svg+xml,%3Csvg width='10' height='6' viewBox='0 0 10 6' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M1 1L5 5L9 1' stroke='%23A8A29E' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") no-repeat right 12px center;
  appearance: none;
  cursor: pointer;
  transition: border-color 0.2s ease;
  min-width: 140px;
}

.filter-select:hover {
  border-color: var(--color-border);
}

.filter-select:focus {
  outline: none;
  border-color: var(--color-accent);
  box-shadow: 0 0 0 3px var(--color-accent-light);
}

/* Assessment Grid */
.assessment-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
  gap: 16px;
}

/* Loading State */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  gap: 16px;
}

.spinner {
  width: 32px;
  height: 32px;
  border: 3px solid var(--color-border);
  border-top-color: var(--color-accent);
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-text {
  font-size: 14px;
  color: var(--color-text-tertiary);
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  text-align: center;
}

.empty-state-icon {
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-accent-light);
  border-radius: var(--radius-full);
  margin-bottom: 20px;
  color: var(--color-accent);
}

.empty-state-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 6px 0;
}

.empty-state-desc {
  font-size: 14px;
  color: var(--color-text-tertiary);
  margin: 0 0 20px 0;
}

/* Modal Form */
.modal-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-label {
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text-secondary);
}

.form-select,
.form-input {
  padding: 10px 14px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  font-size: 14px;
  color: var(--color-text-primary);
  background: #fff;
  transition: all 0.2s ease;
}

.form-select {
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg width='10' height='6' viewBox='0 0 10 6' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M1 1L5 5L9 1' stroke='%23A8A29E' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  padding-right: 32px;
}

.form-select:focus,
.form-input:focus {
  outline: none;
  border-color: var(--color-accent);
  box-shadow: 0 0 0 3px var(--color-accent-light);
}

.form-input::placeholder {
  color: var(--color-text-tertiary);
}

.modal-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 10px;
}

/* Responsive */
@media (max-width: 768px) {
  .assessment-list-page {
    padding: 20px 16px;
  }

  .page-header {
    flex-direction: column;
    gap: 16px;
  }

  .filter-bar {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-group {
    width: 100%;
  }

  .filter-select {
    width: 100%;
    min-width: 0;
  }

  .assessment-grid {
    grid-template-columns: 1fr;
  }
}
</style>
