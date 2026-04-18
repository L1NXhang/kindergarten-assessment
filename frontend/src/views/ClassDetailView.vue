<template>
  <div class="page-container">
    <!-- Class Header -->
    <div class="class-header card mb-lg" v-if="classInfo">
      <div class="flex-between">
        <div>
          <h2 class="class-name">{{ classInfo.name }}</h2>
          <div class="class-meta mt-sm">
            <span class="badge badge-info" v-if="classInfo.age_group">{{ classInfo.age_group }}</span>
            <span class="text-sm text-secondary ml-sm">{{ classInfo.child_count || 0 }} 名幼儿</span>
            <span class="text-sm text-secondary ml-sm">{{ classInfo.anecdote_count || 0 }} 条记录</span>
          </div>
        </div>
        <div class="flex gap-sm">
          <button class="btn btn-primary" @click="handleStartAssessment">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
            发起评估
          </button>
        </div>
      </div>
    </div>

    <!-- Children Table -->
    <div class="card">
      <div class="card-header">
        <h3 class="card-title">幼儿列表</h3>
        <button class="btn btn-secondary btn-sm" @click="showAddChild = true">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
          添加幼儿
        </button>
      </div>

      <div v-if="loading" class="flex-center" style="padding:40px;">
        <span class="loading-spinner"></span>
      </div>

      <BaseTable v-else :columns="tableColumns" :data="children">
        <template #cell-name="{ row }">
          <a class="child-link" @click.prevent="$router.push(`/children/${row.id}`)">{{ row.name }}</a>
        </template>
        <template #cell-gender="{ row }">
          {{ row.gender === 'male' ? '男' : row.gender === 'female' ? '女' : '-' }}
        </template>
        <template #cell-age="{ row }">
          {{ row.birthday ? calcAge(row.birthday) : '-' }}
        </template>
        <template #cell-actions="{ row }">
          <div class="actions">
            <button class="btn btn-ghost btn-sm" @click="$router.push(`/children/${row.id}`)">查看</button>
            <button class="btn btn-ghost btn-sm" @click="handleDeleteChild(row)">删除</button>
          </div>
        </template>
      </BaseTable>
    </div>

    <!-- Add Child Modal -->
    <BaseModal v-model="showAddChild" title="添加幼儿">
      <div class="form-group">
        <label class="form-label">姓名</label>
        <input v-model="childForm.name" class="form-input" placeholder="幼儿姓名" />
      </div>
      <div class="form-group">
        <label class="form-label">性别</label>
        <select v-model="childForm.gender" class="form-select">
          <option value="">请选择</option>
          <option value="male">男</option>
          <option value="female">女</option>
        </select>
      </div>
      <div class="form-group">
        <label class="form-label">出生日期</label>
        <input type="date" v-model="childForm.birthday" class="form-input" />
      </div>
      <template #footer>
        <button class="btn btn-secondary" @click="showAddChild = false">取消</button>
        <button class="btn btn-primary" @click="handleAddChild" :disabled="!childForm.name">添加</button>
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
.class-name {
  font-size: var(--font-size-2xl);
  font-weight: 700;
  color: var(--color-text-primary);
}

.class-meta {
  display: flex;
  align-items: center;
  gap: 8px;
}

.ml-sm {
  margin-left: 8px;
}

.child-link {
  color: var(--color-accent);
  cursor: pointer;
  font-weight: 500;
}

.child-link:hover {
  text-decoration: underline;
}
</style>
