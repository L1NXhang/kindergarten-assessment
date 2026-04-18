<template>
  <div class="class-list-page">
    <!-- Page Header -->
    <div class="page-header">
      <div class="page-header__left">
        <h1 class="page-header__title">班级管理</h1>
        <p class="page-header__subtitle" v-if="classes.length > 0">共 {{ classes.length }} 个班级</p>
      </div>
      <div class="page-header__actions">
        <ExcelUploader @uploaded="handleImport" />
        <button class="btn-create" @click="showCreateModal = true">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
          创建班级
        </button>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="loading-wrapper">
      <span class="loading-spinner"></span>
    </div>

    <!-- Class Cards Grid -->
    <div v-else-if="classes.length > 0" class="class-grid">
      <div
        v-for="cls in classes"
        :key="cls.id"
        class="class-card"
        @click="$router.push(`/classes/${cls.id}`)"
      >
        <div class="class-card__top">
          <h3 class="class-card__name">{{ cls.name }}</h3>
          <div class="class-card__menu">
            <button class="class-card__btn" @click.stop="handleEdit(cls)" title="编辑">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
            </button>
            <button class="class-card__btn class-card__btn--danger" @click.stop="handleDelete(cls)" title="删除">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
            </button>
          </div>
        </div>

        <div class="class-card__body">
          <span class="class-card__badge" v-if="cls.age_group">{{ cls.age_group }}</span>
          <div class="class-card__stats">
            <div class="class-card__stat">
              <span class="class-card__stat-value">{{ cls.child_count || 0 }}</span>
              <span class="class-card__stat-label">幼儿</span>
            </div>
            <div class="class-card__stat-divider"></div>
            <div class="class-card__stat">
              <span class="class-card__stat-value">{{ cls.anecdote_count || 0 }}</span>
              <span class="class-card__stat-label">记录</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <EmptyState v-else title="暂无班级" description="创建您的第一个班级，开始管理幼儿信息">
      <template #action>
        <button class="btn-create" @click="showCreateModal = true">创建班级</button>
      </template>
    </EmptyState>

    <!-- Create/Edit Modal -->
    <BaseModal v-model="showCreateModal" :title="editingClass ? '编辑班级' : '创建班级'">
      <div class="modal-form">
        <div class="form-field">
          <label class="form-field__label">班级名称</label>
          <input v-model="formData.name" class="form-field__input" placeholder="例如：大一班" />
        </div>
        <div class="form-field">
          <label class="form-field__label">年龄段</label>
          <select v-model="formData.age_group" class="form-field__select">
            <option value="">请选择</option>
            <option v-for="group in AGE_GROUPS" :key="group" :value="group">{{ group }}</option>
          </select>
        </div>
      </div>
      <template #footer>
        <button class="btn-cancel" @click="showCreateModal = false">取消</button>
        <button class="btn-primary" @click="handleSave" :disabled="!formData.name">
          {{ editingClass ? '保存' : '创建' }}
        </button>
      </template>
    </BaseModal>

    <!-- Delete Confirm -->
    <ConfirmDialog
      v-model="showDeleteConfirm"
      title="删除班级"
      :message="`确定要删除班级「${deletingClass?.name}」吗？此操作不可恢复。`"
      confirm-text="删除"
      type="danger"
      @confirm="confirmDelete"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { useClassStore } from '../stores/classes.js'
import { useToast } from '../composables/useToast.js'
import BaseModal from '../components/common/BaseModal.vue'
import ConfirmDialog from '../components/common/ConfirmDialog.vue'
import EmptyState from '../components/common/EmptyState.vue'
import ExcelUploader from '../components/common/ExcelUploader.vue'
import { AGE_GROUPS } from '../utils/constants.js'

const classStore = useClassStore()
const toast = useToast()

const loading = ref(false)
const showCreateModal = ref(false)
const showDeleteConfirm = ref(false)
const editingClass = ref(null)
const deletingClass = ref(null)

const formData = reactive({
  name: '',
  age_group: ''
})

const classes = ref([])

onMounted(async () => {
  loading.value = true
  try {
    await classStore.fetchClasses()
    classes.value = classStore.classes
  } catch {
    toast.error('加载班级列表失败')
  } finally {
    loading.value = false
  }
})

function handleEdit(cls) {
  editingClass.value = cls
  formData.name = cls.name
  formData.age_group = cls.age_group || ''
  showCreateModal.value = true
}

function handleDelete(cls) {
  deletingClass.value = cls
  showDeleteConfirm.value = true
}

async function handleSave() {
  if (!formData.name) return
  try {
    if (editingClass.value) {
      await classStore.editClass(editingClass.value.id, { ...formData })
      toast.success('班级已更新')
    } else {
      await classStore.addClass({ ...formData })
      toast.success('班级已创建')
    }
    classes.value = classStore.classes
    showCreateModal.value = false
    resetForm()
  } catch {
    // Error handled by API interceptor
  }
}

async function confirmDelete() {
  if (!deletingClass.value) return
  try {
    await classStore.removeClass(deletingClass.value.id)
    classes.value = classStore.classes
    toast.success('班级已删除')
  } catch {
    // Error handled by API interceptor
  }
}

async function handleImport(file) {
  try {
    await classStore.importExcel(file)
    classes.value = classStore.classes
    toast.success('导入成功')
  } catch {
    toast.error('导入失败')
  }
}

function resetForm() {
  editingClass.value = null
  formData.name = ''
  formData.age_group = ''
}
</script>

<style scoped>
.class-list-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--space-8) var(--space-6);
}

/* ── Page Header ── */
.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: var(--space-8);
}

.page-header__title {
  font-size: 24px;
  font-weight: 700;
  color: var(--color-text-primary);
  letter-spacing: -0.02em;
  line-height: 1.2;
}

.page-header__subtitle {
  margin-top: var(--space-1);
  font-size: 14px;
  color: var(--color-text-tertiary);
}

.page-header__actions {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

/* ── Buttons ── */
.btn-create {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-5);
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

.btn-create:hover {
  background: #4338CA;
  box-shadow: var(--shadow-sm);
}

.btn-create:disabled {
  opacity: 0.5;
  cursor: not-allowed;
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

/* ── Class Grid ── */
.class-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-5);
  animation: fadeIn 0.3s var(--transition-slow) both;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* ── Class Card ── */
.class-card {
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--radius-xl);
  padding: var(--space-6);
  cursor: pointer;
  transition: box-shadow var(--transition-normal), transform var(--transition-normal), border-color var(--transition-normal);
}

.class-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
  border-color: var(--color-border);
}

.class-card__top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: var(--space-4);
}

.class-card__name {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text-primary);
  letter-spacing: -0.01em;
  line-height: 1.3;
}

.class-card__menu {
  display: flex;
  gap: var(--space-1);
  opacity: 0;
  transition: opacity var(--transition-fast);
}

.class-card:hover .class-card__menu {
  opacity: 1;
}

.class-card__btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: var(--color-bg-primary);
  border-radius: var(--radius-md);
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: background-color var(--transition-fast), color var(--transition-fast);
}

.class-card__btn:hover {
  background: var(--color-accent-light);
  color: var(--color-accent);
}

.class-card__btn--danger:hover {
  background: #FEF2F2;
  color: #DC2626;
}

.class-card__body {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.class-card__badge {
  display: inline-flex;
  align-self: flex-start;
  padding: var(--space-1) var(--space-3);
  background: var(--color-accent-light);
  color: var(--color-accent);
  font-size: 12px;
  font-weight: 500;
  border-radius: var(--radius-full);
}

.class-card__stats {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.class-card__stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}

.class-card__stat-value {
  font-size: 20px;
  font-weight: 700;
  color: var(--color-text-primary);
  line-height: 1.2;
}

.class-card__stat-label {
  font-size: 12px;
  color: var(--color-text-tertiary);
}

.class-card__stat-divider {
  width: 1px;
  height: 28px;
  background: var(--color-border-subtle);
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
  padding: var(--space-12);
}

/* ── Responsive ── */
@media (max-width: 1024px) {
  .class-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .class-list-page {
    padding: var(--space-4);
  }

  .page-header {
    flex-direction: column;
    gap: var(--space-4);
    margin-bottom: var(--space-6);
  }

  .page-header__actions {
    width: 100%;
  }

  .class-grid {
    grid-template-columns: 1fr;
    gap: var(--space-3);
  }

  .class-card {
    padding: var(--space-5);
  }

  .class-card__menu {
    opacity: 1;
  }

  .class-card__btn {
    width: 36px;
    height: 36px;
  }
}
</style>
