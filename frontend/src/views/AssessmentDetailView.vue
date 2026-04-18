<template>
  <div class="page-container">
    <div v-if="loading" class="flex-center" style="padding:60px;">
      <span class="loading-spinner"></span>
    </div>

    <template v-else-if="assessment">
      <!-- Assessment Header -->
      <div class="assessment-header card mb-lg">
        <div class="flex-between">
          <div>
            <h2 class="assessment-title">{{ assessment.title || '评估报告' }}</h2>
            <div class="assessment-meta mt-sm">
              <span class="badge" :style="{ background: statusColor + '15', color: statusColor }">
                {{ statusLabel }}
              </span>
              <span class="text-sm text-secondary ml-sm">{{ assessment.class_name }}</span>
              <span class="text-sm text-secondary" v-if="assessment.child_name"> - {{ assessment.child_name }}</span>
              <span class="text-sm text-tertiary ml-sm">{{ formatDate(assessment.created_at) }}</span>
            </div>
          </div>
          <div class="flex gap-sm">
            <button
              v-if="assessment.status === 'pending'"
              class="btn btn-primary"
              @click="handleGenerate"
              :disabled="generating"
            >
              <span v-if="generating" class="loading-spinner" style="width:14px;height:14px;border-width:2px;"></span>
              {{ generating ? '生成中...' : '生成报告' }}
            </button>
            <button
              v-if="assessment.status === 'completed'"
              class="btn btn-secondary"
              @click="handleExport"
            >
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
              导出
            </button>
          </div>
        </div>
      </div>

      <!-- Tabs -->
      <div class="tab-bar">
        <button
          class="tab-item"
          :class="{ active: activeTab === 'report' }"
          @click="activeTab = 'report'"
        >个人报告</button>
        <button
          class="tab-item"
          :class="{ active: activeTab === 'summary' }"
          @click="activeTab = 'summary'"
        >班级汇总</button>
        <button
          class="tab-item"
          :class="{ active: activeTab === 'reflection' }"
          @click="activeTab = 'reflection'"
        >教育反思</button>
      </div>

      <!-- Tab Content -->
      <div class="card">
        <!-- Report Tab -->
        <div v-if="activeTab === 'report'">
          <div v-if="assessment.scores" class="mb-lg">
            <h3 class="card-title mb-md">发展领域雷达图</h3>
            <DomainRadar :scores="assessment.scores" :height="320" />
          </div>
          <div class="mb-lg">
            <h3 class="card-title mb-md">评估报告</h3>
            <ReportViewer :content="assessment.report_content" :loading="false" />
          </div>
        </div>

        <!-- Summary Tab -->
        <div v-if="activeTab === 'summary'">
          <div v-if="assessment.class_summary" class="markdown-content" v-html="renderMarkdown(assessment.class_summary)"></div>
          <EmptyState v-else title="暂无班级汇总" description="班级汇总将在报告生成后显示" />
        </div>

        <!-- Reflection Tab -->
        <div v-if="activeTab === 'reflection'">
          <div v-if="assessment.reflection" class="markdown-content" v-html="renderMarkdown(assessment.reflection)"></div>
          <EmptyState v-else title="暂无教育反思" description="教育反思将在报告生成后显示" />
        </div>
      </div>
    </template>

    <EmptyState v-else title="评估不存在" description="找不到该评估记录" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAssessmentStore } from '../stores/assessments.js'
import { useToast } from '../composables/useToast.js'
import { useExport } from '../composables/useExport.js'
import DomainRadar from '../components/assessment/DomainRadar.vue'
import ReportViewer from '../components/assessment/ReportViewer.vue'
import EmptyState from '../components/common/EmptyState.vue'
import { ASSESSMENT_STATUS } from '../utils/constants.js'
import { formatDate } from '../utils/format.js'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

const route = useRoute()
const assessmentStore = useAssessmentStore()
const toast = useToast()
const { exportReport, exporting } = useExport()

const assessmentId = route.params.id
const assessment = ref(null)
const loading = ref(false)
const generating = ref(false)
const activeTab = ref('report')

const statusInfo = computed(() => {
  return ASSESSMENT_STATUS[assessment.value?.status] || ASSESSMENT_STATUS.pending
})
const statusLabel = computed(() => statusInfo.value.label)
const statusColor = computed(() => statusInfo.value.color)

function renderMarkdown(content) {
  if (!content) return ''
  return DOMPurify.sanitize(marked(content))
}

onMounted(async () => {
  loading.value = true
  try {
    assessment.value = await assessmentStore.fetchAssessmentById(assessmentId)
  } catch {
    toast.error('加载评估失败')
  } finally {
    loading.value = false
  }
})

async function handleGenerate() {
  generating.value = true
  try {
    const result = await assessmentStore.generateAssessmentReport(assessmentId)
    assessment.value = result
    toast.success('报告生成成功')
  } catch {
    toast.error('报告生成失败')
  } finally {
    generating.value = false
  }
}

async function handleExport() {
  await exportReport(assessmentId, 'pdf', `评估报告-${assessment.value?.title || assessmentId}`)
}
</script>

<style scoped>
.assessment-title {
  font-size: var(--font-size-2xl);
  font-weight: 700;
  color: var(--color-text-primary);
}

.assessment-meta {
  display: flex;
  align-items: center;
  gap: 8px;
}

.ml-sm {
  margin-left: 8px;
}
</style>
