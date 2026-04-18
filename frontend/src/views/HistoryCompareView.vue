<template>
  <div class="page-container">
    <div class="page-header">
      <h2>历史对比</h2>
    </div>

    <!-- Selection Panel -->
    <div class="card mb-lg">
      <div class="card-header">
        <h3 class="card-title">选择对比对象</h3>
      </div>
      <div class="compare-form">
        <div class="form-group">
          <label class="form-label">对比类型</label>
          <select v-model="compareType" class="form-select" style="width:200px;">
            <option value="child">幼儿对比</option>
            <option value="class">班级对比</option>
          </select>
        </div>

        <div class="form-group" v-if="compareType === 'child'">
          <label class="form-label">选择幼儿</label>
          <ChildSelector v-model="selectedChildId" :children="allChildren" />
        </div>

        <div class="form-group" v-if="compareType === 'class'">
          <label class="form-label">选择班级</label>
          <select v-model="selectedClassId" class="form-select" style="width:200px;">
            <option value="">请选择</option>
            <option v-for="cls in classes" :key="cls.id" :value="cls.id">{{ cls.name }}</option>
          </select>
        </div>

        <div class="form-group">
          <label class="form-label">第一次评估</label>
          <select v-model="assessment1Id" class="form-select" style="width:300px;">
            <option value="">请选择</option>
            <option v-for="a in assessmentList" :key="a.id" :value="a.id">
              {{ a.title || '评估' }} - {{ formatDate(a.created_at) }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label class="form-label">第二次评估</label>
          <select v-model="assessment2Id" class="form-select" style="width:300px;">
            <option value="">请选择</option>
            <option v-for="a in assessmentList" :key="a.id" :value="a.id">
              {{ a.title || '评估' }} - {{ formatDate(a.created_at) }}
            </option>
          </select>
        </div>

        <button
          class="btn btn-primary"
          @click="handleCompare"
          :disabled="!canCompare || loading"
        >
          <span v-if="loading" class="loading-spinner" style="width:14px;height:14px;border-width:2px;"></span>
          开始对比
        </button>
      </div>
    </div>

    <!-- Comparison Result -->
    <div v-if="comparisonData" class="grid grid-2 mb-lg">
      <!-- Radar Comparison -->
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">雷达图对比</h3>
        </div>
        <DomainRadar :scores="comparisonData.scores1 || {}" :height="300" />
      </div>

      <!-- Trend Chart -->
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">趋势变化</h3>
        </div>
        <TrendChart
          :labels="trendLabels"
          :datasets="trendDatasets"
          :height="300"
        />
      </div>
    </div>

    <!-- Score Comparison Table -->
    <div class="card" v-if="comparisonData">
      <div class="card-header">
        <h3 class="card-title">分数对比</h3>
      </div>
      <BaseTable :columns="scoreColumns" :data="scoreRows">
        <template #cell-change="{ row }">
          <span :class="getChangeClass(row.change)">
            {{ formatChange(row.change) }}
          </span>
        </template>
      </BaseTable>
    </div>

    <EmptyState
      v-if="!comparisonData && !loading"
      title="选择评估进行对比"
      description="选择两次评估来查看幼儿或班级的发展变化趋势"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useClassStore } from '../stores/classes.js'
import { useAssessmentStore } from '../stores/assessments.js'
import { useChildStore } from '../stores/children.js'
import { useToast } from '../composables/useToast.js'
import ChildSelector from '../components/child/ChildSelector.vue'
import DomainRadar from '../components/assessment/DomainRadar.vue'
import TrendChart from '../components/assessment/TrendChart.vue'
import BaseTable from '../components/common/BaseTable.vue'
import EmptyState from '../components/common/EmptyState.vue'
import { DOMAINS } from '../utils/constants.js'
import { formatDate } from '../utils/format.js'

const classStore = useClassStore()
const assessmentStore = useAssessmentStore()
const childStore = useChildStore()
const toast = useToast()

const compareType = ref('child')
const selectedChildId = ref('')
const selectedClassId = ref('')
const assessment1Id = ref('')
const assessment2Id = ref('')
const classes = ref([])
const allChildren = ref([])
const assessmentList = ref([])
const comparisonData = ref(null)
const loading = ref(false)

const canCompare = computed(() => {
  return assessment1Id.value && assessment2Id.value && assessment1Id.value !== assessment2Id.value
})

const scoreColumns = [
  { key: 'domain', label: '领域' },
  { key: 'score1', label: '第一次', width: '100px' },
  { key: 'score2', label: '第二次', width: '100px' },
  { key: 'change', label: '变化', width: '100px' }
]

const trendLabels = computed(() => {
  if (!comparisonData.value) return []
  return ['健康', '语言', '社会', '科学', '艺术']
})

const trendDatasets = computed(() => {
  if (!comparisonData.value) return []
  const s1 = comparisonData.value.scores1 || {}
  const s2 = comparisonData.value.scores2 || {}
  return [
    {
      label: '第一次',
      data: DOMAINS.map(d => s1[d.key] || 0),
      borderColor: '#2563EB',
      backgroundColor: 'rgba(37,99,235,0.1)'
    },
    {
      label: '第二次',
      data: DOMAINS.map(d => s2[d.key] || 0),
      borderColor: '#10B981',
      backgroundColor: 'rgba(16,185,129,0.1)'
    }
  ]
})

const scoreRows = computed(() => {
  if (!comparisonData.value) return []
  const s1 = comparisonData.value.scores1 || {}
  const s2 = comparisonData.value.scores2 || {}
  return DOMAINS.map(d => ({
    domain: d.name,
    score1: s1[d.key] ?? '-',
    score2: s2[d.key] ?? '-',
    change: (s2[d.key] || 0) - (s1[d.key] || 0)
  }))
})

function getChangeClass(change) {
  if (change > 0) return 'change-positive'
  if (change < 0) return 'change-negative'
  return 'change-neutral'
}

function formatChange(change) {
  if (change > 0) return `+${change}`
  if (change < 0) return `${change}`
  return '0'
}

onMounted(async () => {
  try {
    await classStore.fetchClasses()
    classes.value = classStore.classes
  } catch {
    // Silent
  }

  try {
    await childStore.fetchChildren()
    allChildren.value = childStore.children
  } catch {
    // Silent
  }

  try {
    await assessmentStore.fetchAssessments({ status: 'completed' })
    assessmentList.value = assessmentStore.assessments
  } catch {
    // Silent
  }
})

watch([compareType, selectedChildId, selectedClassId], () => {
  assessment1Id.value = ''
  assessment2Id.value = ''
  comparisonData.value = null

  // Filter assessments based on selection
  if (compareType.value === 'child' && selectedChildId.value) {
    assessmentList.value = assessmentStore.assessments.filter(
      a => a.child_id == selectedChildId.value
    )
  } else if (compareType.value === 'class' && selectedClassId.value) {
    assessmentList.value = assessmentStore.assessments.filter(
      a => a.class_id == selectedClassId.value
    )
  } else {
    assessmentList.value = assessmentStore.assessments
  }
})

async function handleCompare() {
  if (!canCompare.value) return
  loading.value = true
  try {
    const result = await assessmentStore.fetchComparison({
      assessment1_id: assessment1Id.value,
      assessment2_id: assessment2Id.value
    })
    comparisonData.value = result
  } catch {
    toast.error('对比分析失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.compare-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-width: 600px;
}

.change-positive {
  color: var(--color-success);
  font-weight: 600;
}

.change-negative {
  color: var(--color-danger);
  font-weight: 600;
}

.change-neutral {
  color: var(--color-text-tertiary);
}
</style>
