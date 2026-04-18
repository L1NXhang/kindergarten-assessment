<template>
  <div class="page-container">
    <div class="page-header">
      <h2>班级管理</h2>
      <div class="page-header-actions">
        <ExcelUploader @uploaded="handleImport" />
        <button class="btn btn-primary" @click="showCreateModal = true">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
          创建班级
        </button>
      </div>
    </div>

    <div v-if="loading" class="flex-center" style="padding:60px;">
      <span class="loading-spinner"></span>
    </div>

    <div v-else-if="classes.length > 0" class="grid grid-3">
      <div
        v-for="cls in classes"
        :key="cls.id"
        class="class-card card"
        @click="$router.push(`/classes/${cls.id}`)"
      >
        <div class="class-card-header">
          <h3 class="class-card-name">{{ cls.name }}</h3>
          <div class="class-card-menu">
            <button class="btn btn-ghost btn-icon btn-sm" @click.stop="handleEdit(cls)">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
            </button>
            <button class="btn btn-ghost btn-icon btn-sm" @click.stop="handleDelete(cls)">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
            </button>
          </div>
        </div>
        <div class="class-card-body">
          <div class="class-card-info">
            <span class="badge badge-info" v-if="cls.age_group">{{ cls.age_group }}</span>
          </div>
          <div class="class-card-stats">
            <div class="class-stat">
              <span class="class-stat-value">{{ cls.child_count || 0 }}</span>
              <span class="class-stat-label">幼儿</span>
            </div>
            <div class="class-stat">
              <span class="class-stat-value">{{ cls.anecdote_count || 0 }}</span>
              <span class="class-stat-label">记录</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <EmptyState v-else title="暂无班级" description="创建您的第一个班级，开始管理幼儿信息">
      <template #action>
        <button class="btn btn-primary" @click="showCreateModal = true">创建班级</button>
      </template>
    </EmptyState>

    <!-- Create/Edit Modal -->
    <BaseModal v-model="showCreateModal" :title="editingClass ? '编辑班级' : '创建班级'">
      <div class="form-group">
        <label class="form-label">班级名称</label>
        <input v-model="formData.name" class="form-input" placeholder="例如：大一班" />
      </div>
      <div class="form-group">
        <label class="form-label">年龄段</label>
        <select v-model="formData.age_group" class="form-select">
          <option value="">请选择</option>
          <option v-for="group in AGE_GROUPS" :key="group" :value="group">{{ group }}</option>
        </select>
      </div>
      <template #footer>
        <button class="btn btn-secondary" @click="showCreateModal = false">取消</button>
        <button class="btn btn-primary" @click="handleSave" :disabled="!formData.name">
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
.class-card {
  cursor: pointer;
  transition: all 0.15s ease;
}

.class-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.class-card-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 12px;
}

.class-card-name {
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--color-text-primary);
}

.class-card-menu {
  display: flex;
  gap: 2px;
}

.class-card-body {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.class-card-info {
  display: flex;
  gap: 6px;
}

.class-card-stats {
  display: flex;
  gap: 16px;
}

.class-stat {
  text-align: center;
}

.class-stat-value {
  display: block;
  font-size: var(--font-size-lg);
  font-weight: 700;
  color: var(--color-text-primary);
}

.class-stat-label {
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
}
</style>
