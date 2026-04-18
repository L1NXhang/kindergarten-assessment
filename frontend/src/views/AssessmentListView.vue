<template>
  <div class="page-container">
    <div class="page-header">
      <h2>阶段性评估</h2>
      <div class="page-header-actions">
        <button class="btn btn-primary" @click="showNewModal = true">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
          新建评估
        </button>
      </div>
    </div>

    <!-- Filters -->
    <div class="filter-bar">
      <select v-model="filters.status" class="form-select" @change="handleFilter">
        <option value="">全部状态</option>
        <option v-for="(info, key) in ASSESSMENT_STATUS" :key="key" :value="key">{{ info.label }}</option>
      </select>
      <select v-model="filters.class_id" class="form-select" @change="handleFilter">
        <option value="">全部班级</option>
        <option v-for="cls in classes" :key="cls.id" :value="cls.id">{{ cls.name }}</option>
      </select>
    </div>

    <!-- Assessment List -->
    <div v-if="loading" class="flex-center" style="padding:60px;">
      <span class="loading-spinner"></span>
    </div>

    <div v-else-if="assessments.length > 0" class="assessment-list">
      <AssessmentCard
        v-for="item in assessments"
        :key="item.id"
        :assessment="item"
        @click="$router.push(`/assessments/${item.id}`)"
      />
    </div>

    <EmptyState v-else title="暂无评估" description="创建新的评估来生成发展报告">
      <template #action>
        <button class="btn btn-primary" @click="showNewModal = true">新建评估</button>
      </template>
    </EmptyState>

    <!-- New Assessment Modal -->
    <BaseModal v-model="showNewModal" title="新建评估">
      <div class="form-group">
        <label class="form-label">评估类型</label>
        <select v-model="newForm.type" class="form-select">
          <option value="class">班级评估</option>
          <option value="personal">个人评估</option>
        </select>
      </div>
      <div class="form-group">
        <label class="form-label">{{ newForm.type === 'class' ? '选择班级' : '选择幼儿' }}</label>
        <select v-model="newForm.target_id" class="form-select">
          <option value="">请选择</option>
          <option v-if="newForm.type === 'class'" v-for="cls in classes" :key="cls.id" :value="cls.id">{{ cls.name }}</option>
        </select>
      </div>
      <div class="form-group">
        <label class="form-label">评估周期</label>
        <input type="text" v-model="newForm.period" class="form-input" placeholder="例如：2024年上学期" />
      </div>
      <template #footer>
        <button class="btn btn-secondary" @click="showNewModal = false">取消</button>
        <button class="btn btn-primary" @click="handleCreate" :disabled="!newForm.target_id">创建并生成</button>
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
.assessment-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
  gap: 12px;
}
</style>
