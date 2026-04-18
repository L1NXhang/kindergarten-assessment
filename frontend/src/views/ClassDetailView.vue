<template>
  <div class="class-detail-page">
    <!-- Class Header -->
    <div class="class-header" v-if="classInfo">
      <div class="class-header__left">
        <div class="class-header__breadcrumb">
          <router-link to="/classes" class="class-header__back">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"/></svg>
            班级管理
          </router-link>
        </div>
        <h1 class="class-header__name">{{ classInfo.name }}</h1>
        <div class="class-header__meta">
          <span class="class-header__badge" v-if="classInfo.age_group">{{ classInfo.age_group }}</span>
          <span class="class-header__stat">{{ classInfo.child_count || 0 }} 名幼儿</span>
          <span class="class-header__stat-divider"></span>
          <span class="class-header__stat">{{ classInfo.anecdote_count || 0 }} 条记录</span>
        </div>
      </div>
      <div class="class-header__actions">
        <button class="btn-accent" @click="handleStartAssessment">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
          发起评估
        </button>
      </div>
    </div>

    <!-- Children Table -->
    <div class="children-section">
      <div class="children-section__header">
        <h2 class="children-section__title">幼儿列表</h2>
        <button class="btn-outline" @click="showAddChild = true">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
          添加幼儿
        </button>
      </div>

      <div v-if="loading" class="loading-wrapper">
        <span class="loading-spinner"></span>
      </div>

      <div v-else class="table-wrapper">
        <BaseTable :columns="tableColumns" :data="children">
          <template #cell-name="{ row }">
            <a class="child-name-link" @click.prevent="$router.push(`/children/${row.id}`)">{{ row.name }}</a>
          </template>
          <template #cell-gender="{ row }">
            <span class="gender-tag" :class="row.gender === 'male' ? 'gender-tag--male' : row.gender === 'female' ? 'gender-tag--female' : ''">
              {{ row.gender === 'male' ? '男' : row.gender === 'female' ? '女' : '-' }}
            </span>
          </template>
          <template #cell-age="{ row }">
            <span class="table-cell-text">{{ row.birthday ? calcAge(row.birthday) : '-' }}</span>
          </template>
          <template #cell-anecdote_count="{ row }">
            <span class="table-cell-text">{{ row.anecdote_count || 0 }}</span>
          </template>
          <template #cell-actions="{ row }">
            <div class="row-actions">
              <button class="row-actions__btn" @click="$router.push(`/children/${row.id}`)">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                查看
              </button>
              <button class="row-actions__btn row-actions__btn--danger" @click="handleDeleteChild(row)">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
                删除
              </button>
            </div>
          </template>
        </BaseTable>
      </div>
    </div>

    <!-- Add Child Modal -->
    <BaseModal v-model="showAddChild" title="添加幼儿">
      <div class="modal-form">
        <div class="form-field">
          <label class="form-field__label">姓名</label>
          <input v-model="childForm.name" class="form-field__input" placeholder="幼儿姓名" />
        </div>
        <div class="form-field">
          <label class="form-field__label">性别</label>
          <select v-model="childForm.gender" class="form-field__select">
            <option value="">请选择</option>
            <option value="male">男</option>
            <option value="female">女</option>
          </select>
        </div>
        <div class="form-field">
          <label class="form-field__label">出生日期</label>
          <input type="date" v-model="childForm.birthday" class="form-field__input" />
        </div>
      </div>
      <template #footer>
        <button class="btn-cancel" @click="showAddChild = false">取消</button>
        <button class="btn-primary" @click="handleAddChild" :disabled="!childForm.name">添加</button>
      </template>
    </BaseModal>

    <!-- Delete Confirm -->
    <ConfirmDialog
      v-model="showDeleteConfirm"
      title="删除幼儿"
      :message="`确定要删除幼儿「${deletingChild?.name}」吗？`"
      confirm-text="删除"
      type="danger"
      @confirm="confirmDeleteChild"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useClassStore } from '../stores/classes.js'
import { useChildStore } from '../stores/children.js'
import { useAssessmentStore } from '../stores/assessments.js'
import { useToast } from '../composables/useToast.js'
import BaseTable from '../components/common/BaseTable.vue'
import BaseModal from '../components/common/BaseModal.vue'
import ConfirmDialog from '../components/common/ConfirmDialog.vue'
import { calcAge } from '../utils/format.js'

const route = useRoute()
const router = useRouter()
const classStore = useClassStore()
const childStore = useChildStore()
const assessmentStore = useAssessmentStore()
const toast = useToast()

const classId = route.params.id
const classInfo = ref(null)
const children = ref([])
const loading = ref(false)
const showAddChild = ref(false)
const showDeleteConfirm = ref(false)
const deletingChild = ref(null)

const childForm = reactive({
  name: '',
  gender: '',
  birthday: ''
})

const tableColumns = [
  { key: 'name', label: '姓名' },
  { key: 'gender', label: '性别', width: '80px' },
  { key: 'age', label: '年龄', width: '80px' },
  { key: 'anecdote_count', label: '记录数', width: '80px' },
  { key: 'actions', label: '操作', width: '120px' }
]

onMounted(async () => {
  loading.value = true
  try {
    classInfo.value = await classStore.fetchClassById(classId)
    const classChildren = await import('../api/classes.js').then(m => m.getClassChildren(classId))
    children.value = classChildren || []
  } catch {
    toast.error('加载班级信息失败')
  } finally {
    loading.value = false
  }
})

async function handleAddChild() {
  if (!childForm.name) return
  try {
    const result = await childStore.addChild({
      ...childForm,
      class_id: classId
    })
    children.value.push(result)
    showAddChild.value = false
    childForm.name = ''
    childForm.gender = ''
    childForm.birthday = ''
    toast.success('幼儿已添加')
  } catch {
    // Error handled by interceptor
  }
}

function handleDeleteChild(child) {
  deletingChild.value = child
  showDeleteConfirm.value = true
}

async function confirmDeleteChild() {
  if (!deletingChild.value) return
  try {
    await childStore.removeChild(deletingChild.value.id)
    children.value = children.value.filter(c => c.id !== deletingChild.value.id)
    toast.success('幼儿已删除')
  } catch {
    // Error handled by interceptor
  }
}

async function handleStartAssessment() {
  try {
    const assessment = await assessmentStore.addAssessment({
      class_id: classId,
      type: 'class'
    })
    router.push(`/assessments/${assessment.id}`)
  } catch {
    // Error handled by interceptor
  }
}
</script>

<style scoped>
.class-detail-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--space-8) var(--space-6);
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

/* ── Class Header ── */
.class-header {
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--radius-xl);
  padding: var(--space-8);
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  animation: fadeInUp 0.3s var(--transition-slow) both;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.class-header__left {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.class-header__breadcrumb {
  margin-bottom: var(--space-1);
}

.class-header__back {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  font-size: 13px;
  color: var(--color-text-tertiary);
  text-decoration: none;
  transition: color var(--transition-fast);
}

.class-header__back:hover {
  color: var(--color-accent);
}

.class-header__name {
  font-size: 28px;
  font-weight: 700;
  color: var(--color-text-primary);
  letter-spacing: -0.02em;
  line-height: 1.2;
}

.class-header__meta {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin-top: var(--space-1);
}

.class-header__badge {
  display: inline-flex;
  padding: var(--space-1) var(--space-3);
  background: var(--color-accent-light);
  color: var(--color-accent);
  font-size: 12px;
  font-weight: 500;
  border-radius: var(--radius-full);
}

.class-header__stat {
  font-size: 14px;
  color: var(--color-text-secondary);
}

.class-header__stat-divider {
  width: 1px;
  height: 14px;
  background: var(--color-border);
}

.class-header__actions {
  flex-shrink: 0;
}

/* ── Buttons ── */
.btn-accent {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-6);
  background: var(--color-accent);
  color: #FFFFFF;
  border: none;
  border-radius: var(--radius-lg);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color var(--transition-fast), box-shadow var(--transition-fast);
  white-space: nowrap;
}

.btn-accent:hover {
  background: #4338CA;
  box-shadow: var(--shadow-sm);
}

.btn-outline {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-4);
  background: transparent;
  color: var(--color-text-primary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: border-color var(--transition-fast), background-color var(--transition-fast);
}

.btn-outline:hover {
  border-color: var(--color-accent);
  background: var(--color-accent-light);
  color: var(--color-accent);
}

.btn-cancel {
  display: inline-flex;
  align-items: center;
  padding: var(--space-2) var(--space-5);
  background: transparent;
  color: var(--color-text-secondary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color var(--transition-fast), border-color var(--transition-fast);
}

.btn-cancel:hover {
  background: var(--color-bg-primary);
  border-color: var(--color-text-tertiary);
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  padding: var(--space-2) var(--space-5);
  background: var(--color-accent);
  color: #FFFFFF;
  border: none;
  border-radius: var(--radius-lg);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color var(--transition-fast);
}

.btn-primary:hover {
  background: #4338CA;
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* ── Children Section ── */
.children-section {
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--radius-xl);
  padding: var(--space-6);
  animation: fadeInUp 0.3s var(--transition-slow) 80ms both;
}

.children-section__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-5);
}

.children-section__title {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
  letter-spacing: -0.01em;
}

/* ── Table Styles ── */
.table-wrapper {
  overflow-x: auto;
}

.child-name-link {
  color: var(--color-accent);
  cursor: pointer;
  font-weight: 500;
  text-decoration: none;
  transition: color var(--transition-fast);
}

.child-name-link:hover {
  color: #3730A3;
  text-decoration: underline;
}

.gender-tag {
  display: inline-flex;
  align-items: center;
  padding: 2px var(--space-2);
  border-radius: var(--radius-full);
  font-size: 12px;
  font-weight: 500;
}

.gender-tag--male {
  background: #EEF2FF;
  color: #4F46E5;
}

.gender-tag--female {
  background: #FDF2F8;
  color: #DB2777;
}

.table-cell-text {
  color: var(--color-text-secondary);
  font-size: 14px;
}

/* ── Row Actions ── */
.row-actions {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.row-actions__btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: var(--space-1) var(--space-2);
  background: transparent;
  border: none;
  border-radius: var(--radius-md);
  color: var(--color-text-secondary);
  font-size: 13px;
  cursor: pointer;
  transition: background-color var(--transition-fast), color var(--transition-fast);
}

.row-actions__btn:hover {
  background: var(--color-accent-light);
  color: var(--color-accent);
}

.row-actions__btn--danger:hover {
  background: #FEF2F2;
  color: #DC2626;
}

/* ── Modal Form ── */
.modal-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.form-field__label {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-primary);
}

.form-field__input,
.form-field__select {
  padding: var(--space-3) var(--space-4);
  background: var(--color-bg-primary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  font-size: 14px;
  color: var(--color-text-primary);
  transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
  outline: none;
}

.form-field__input:focus,
.form-field__select:focus {
  border-color: var(--color-accent);
  box-shadow: 0 0 0 3px var(--color-accent-light);
}

.form-field__input::placeholder {
  color: var(--color-text-tertiary);
}

/* ── Loading ── */
.loading-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-10);
}

/* ── Responsive ── */
@media (max-width: 768px) {
  .class-detail-page {
    padding: var(--space-4);
    gap: var(--space-4);
  }

  .class-header {
    flex-direction: column;
    gap: var(--space-5);
    padding: var(--space-5);
  }

  .class-header__name {
    font-size: 22px;
  }

  .class-header__actions {
    width: 100%;
  }

  .btn-accent {
    width: 100%;
    justify-content: center;
  }

  .children-section {
    padding: var(--space-4);
  }

  .children-section__header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--space-3);
  }

  .row-actions {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
