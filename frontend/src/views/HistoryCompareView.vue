<template>
  <div class="compare-page">
    <!-- Page Title -->
    <div class="compare-page__title">
      <h1>历史对比</h1>
      <p class="compare-page__subtitle">选择两次评估，查看发展变化趋势</p>
    </div>

    <!-- Selection Panel -->
    <div class="selection-card">
      <h3 class="section-title">选择对比对象</h3>
      <div class="selection-form">
        <div class="form-row">
          <div class="form-field">
            <label class="form-label">对比类型</label>
            <select v-model="compareType" class="form-select">
              <option value="child">幼儿对比</option>
              <option value="class">班级对比</option>
            </select>
          </div>

          <div class="form-field" v-if="compareType === 'child'">
            <label class="form-label">选择幼儿</label>
            <ChildSelector v-model="selectedChildId" :children="allChildren" />
          </div>

          <div class="form-field" v-if="compareType === 'class'">
            <label class="form-label">选择班级</label>
            <select v-model="selectedClassId" class="form-select">
              <option value="">请选择</option>
              <option v-for="cls in classes" :key="cls.id" :value="cls.id">{{ cls.name }}</option>
            </select>
          </div>
        </div>

        <div class="form-row">
          <div class="form-field form-field--grow">
            <label class="form-label">第一次评估</label>
            <select v-model="assessment1Id" class="form-select">
              <option value="">请选择</option>
              <option v-for="a in assessmentList" :key="a.id" :value="a.id">
                {{ a.title || '评估' }} - {{ formatDate(a.created_at) }}
              </option>
            </select>
          </div>

          <div class="form-field form-field--grow">
            <label class="form-label">第二次评估</label>
            <select v-model="assessment2Id" class="form-select">
              <option value="">请选择</option>
              <option v-for="a in assessmentList" :key="a.id" :value="a.id">
                {{ a.title || '评估' }} - {{ formatDate(a.created_at) }}
              </option>
            </select>
          </div>
        </div>

        <button
          class="compare-btn"
          @click="handleCompare"
          :disabled="!canCompare || loading"
        >
          <span v-if="loading" class="compare-btn__spinner"></span>
          {{ loading ? '对比中...' : '开始对比' }}
        </button>
      </div>
    </div>

    <!-- Comparison Results -->
    <template v-if="comparisonData">
      <div class="charts-grid">
        <div class="chart-card">
          <h3 class="section-title">雷达图对比</h3>
          <DomainRadar :scores="comparisonData.scores1 || {}" :height="300" />
        </div>

        <div class="chart-card">
          <h3 class="section-title">趋势变化</h3>
          <TrendChart
            :labels="trendLabels"
            :datasets="trendDatasets"
            :height="300"
          />
        </div>
      </div>

      <!-- Score Comparison Table -->
      <div class="table-card">
        <h3 class="section-title">分数对比</h3>
        <div class="score-table-wrapper">
          <table class="score-table">
            <thead>
              <tr>
                <th>领域</th>
                <th>第一次</th>
                <th>第二次</th>
                <th>变化</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in scoreRows" :key="row.domain">
                <td class="score-table__domain">{{ row.domain }}</td>
                <td class="score-table__num">{{ row.score1 }}</td>
                <td class="score-table__num">{{ row.score2 }}</td>
                <td>
                  <span :class="getChangeClass(row.change)">
                    {{ formatChange(row.change) }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>

    <!-- Empty State -->
    <div class="empty-state" v-if="!comparisonData && !loading">
      <div class="empty-state__icon">
        <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
          <rect x="4" y="8" width="40" height="32" rx="4" stroke="var(--color-text-tertiary)" stroke-width="2"/>
          <path d="M4 18h40" stroke="var(--color-text-tertiary)" stroke-width="2"/>
          <circle cx="14" cy="13" r="2" fill="var(--color-text-tertiary)"/>
          <circle cx="22" cy="13" r="2" fill="var(--color-text-tertiary)"/>
          <circle cx="30" cy="13" r="2" fill="var(--color-text-tertiary)"/>
          <path d="M16 28l5 5 11-11" stroke="var(--color-accent)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>
      <h4 class="empty-state__title">选择评估进行对比</h4>
      <p class="empty-state__desc">选择两次评估来查看幼儿或班级的发展变化趋势</p>
    </div>
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
.compare-page {
  max-width: 960px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* ---- Page Title ---- */
.compare-page__title {
  margin-bottom: 0;
}

.compare-page__title h1 {
  font-size: 24px;
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0 0 4px 0;
}

.compare-page__subtitle {
  font-size: 14px;
  color: var(--color-text-tertiary);
  margin: 0;
}

/* ---- Selection Card ---- */
.selection-card {
  background: #fff;
  border-radius: var(--radius-xl);
  padding: 28px;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border);
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 20px 0;
}

.selection-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-row {
  display: flex;
  gap: 16px;
  align-items: flex-end;
}

.form-field {
  flex: 1;
  min-width: 0;
}

.form-field--grow {
  flex: 2;
}

.form-label {
  display: block;
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text-secondary);
  margin-bottom: 6px;
}

.form-select {
  width: 100%;
  padding: 9px 12px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  font-size: 14px;
  color: var(--color-text-primary);
  background: #fff;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg width='10' height='6' viewBox='0 0 10 6' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M1 1l4 4 4-4' stroke='%23A8A29E' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  padding-right: 32px;
  cursor: pointer;
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
  box-sizing: border-box;
}

.form-select:focus {
  outline: none;
  border-color: var(--color-accent);
  box-shadow: 0 0 0 3px var(--color-accent-light);
}

.compare-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  align-self: flex-start;
  padding: 10px 28px;
  border: none;
  border-radius: var(--radius-md);
  font-size: 14px;
  font-weight: 600;
  color: #fff;
  background: var(--color-accent);
  cursor: pointer;
  transition: background 0.15s ease, box-shadow 0.15s ease;
}

.compare-btn:hover:not(:disabled) {
  background: #4338CA;
  box-shadow: 0 2px 8px rgba(79, 70, 229, 0.3);
}

.compare-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.compare-btn__spinner {
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ---- Charts Grid ---- */
.charts-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.chart-card {
  background: #fff;
  border-radius: var(--radius-xl);
  padding: 24px;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border);
}

/* ---- Score Table ---- */
.table-card {
  background: #fff;
  border-radius: var(--radius-xl);
  padding: 24px;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border);
}

.score-table-wrapper {
  overflow-x: auto;
}

.score-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.score-table thead th {
  text-align: left;
  padding: 10px 16px;
  font-weight: 600;
  font-size: 13px;
  color: var(--color-text-tertiary);
  border-bottom: 1px solid var(--color-border);
  white-space: nowrap;
}

.score-table tbody td {
  padding: 12px 16px;
  color: var(--color-text-primary);
  border-bottom: 1px solid var(--color-border);
}

.score-table tbody tr:last-child td {
  border-bottom: none;
}

.score-table tbody tr:hover {
  background: var(--color-accent-light);
}

.score-table__domain {
  font-weight: 500;
}

.score-table__num {
  font-variant-numeric: tabular-nums;
  text-align: center;
}

.change-positive {
  color: #10B981;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 2px;
}

.change-negative {
  color: #EF4444;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 2px;
}

.change-neutral {
  color: var(--color-text-tertiary);
}

/* ---- Empty State ---- */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 24px;
  text-align: center;
  background: #fff;
  border-radius: var(--radius-xl);
  border: 1px dashed var(--color-border);
}

.empty-state__icon {
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-state__title {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 6px 0;
}

.empty-state__desc {
  font-size: 14px;
  color: var(--color-text-tertiary);
  margin: 0;
  max-width: 320px;
}

/* ---- Responsive ---- */
@media (max-width: 768px) {
  .charts-grid {
    grid-template-columns: 1fr;
  }

  .form-row {
    flex-direction: column;
    align-items: stretch;
  }

  .form-field--grow {
    flex: 1;
  }
}

@media (max-width: 480px) {
  .compare-page {
    gap: 16px;
  }

  .selection-card,
  .chart-card,
  .table-card {
    padding: 16px;
    border-radius: var(--radius-lg);
  }

  .compare-btn {
    width: 100%;
  }
}
</style>
