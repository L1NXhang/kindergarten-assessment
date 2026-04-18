<template>
  <div class="assessment-detail-page">
    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <span class="loading-text">加载评估详情...</span>
    </div>

    <template v-else-if="assessment">
      <!-- Assessment Header -->
      <div class="detail-header">
        <div class="header-content">
          <div class="header-info">
            <h1 class="detail-title">{{ assessment.title || '评估报告' }}</h1>
            <div class="header-meta">
              <span class="status-pill" :style="{ background: statusColor + '14', color: statusColor }">
                {{ statusLabel }}
              </span>
              <span class="meta-divider"></span>
              <span class="meta-text">{{ assessment.class_name }}</span>
              <span v-if="assessment.child_name" class="meta-text">- {{ assessment.child_name }}</span>
              <span class="meta-divider"></span>
              <span class="meta-text meta-date">{{ formatDate(assessment.created_at) }}</span>
            </div>
          </div>
          <div class="header-actions">
            <button
              v-if="assessment.status === 'pending'"
              class="btn-primary"
              @click="handleGenerate"
              :disabled="generating"
            >
              <span v-if="generating" class="btn-spinner"></span>
              {{ generating ? '生成中...' : '生成报告' }}
            </button>
            <button
              v-if="assessment.status === 'completed'"
              class="btn-secondary"
              @click="handleExport"
            >
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
              导出
            </button>
          </div>
        </div>
      </div>

      <!-- Tab Bar -->
      <div class="tab-bar">
        <button
          class="tab-item"
          :class="{ active: activeTab === 'report' }"
          @click="activeTab = 'report'"
        >
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
          个人报告
        </button>
        <button
          class="tab-item"
          :class="{ active: activeTab === 'summary' }"
          @click="activeTab = 'summary'"
        >
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
          班级汇总
        </button>
        <button
          class="tab-item"
          :class="{ active: activeTab === 'reflection' }"
          @click="activeTab = 'reflection'"
        >
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
          教育反思
        </button>
      </div>

      <!-- Tab Content -->
      <div class="tab-content">
        <!-- Report Tab -->
        <div v-if="activeTab === 'report'" class="tab-panel">
          <div v-if="assessment.scores" class="chart-section">
            <h3 class="section-title">发展领域雷达图</h3>
            <div class="chart-wrapper">
              <DomainRadar :scores="assessment.scores" :height="320" />
            </div>
          </div>
          <div class="report-section">
            <h3 class="section-title">评估报告</h3>
            <ReportViewer :content="assessment.report_content" :loading="false" />
          </div>
        </div>

        <!-- Summary Tab -->
        <div v-if="activeTab === 'summary'" class="tab-panel">
          <div v-if="assessment.class_summary" class="markdown-content" v-html="renderMarkdown(assessment.class_summary)"></div>
          <div v-else class="tab-empty">
            <div class="tab-empty-icon">
              <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
            </div>
            <h3 class="tab-empty-title">暂无班级汇总</h3>
            <p class="tab-empty-desc">班级汇总将在报告生成后显示</p>
          </div>
        </div>

        <!-- Reflection Tab -->
        <div v-if="activeTab === 'reflection'" class="tab-panel">
          <div v-if="assessment.reflection" class="markdown-content" v-html="renderMarkdown(assessment.reflection)"></div>
          <div v-else class="tab-empty">
            <div class="tab-empty-icon">
              <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
            </div>
            <h3 class="tab-empty-title">暂无教育反思</h3>
            <p class="tab-empty-desc">教育反思将在报告生成后显示</p>
          </div>
        </div>
      </div>
    </template>

    <!-- Not Found State -->
    <div v-else class="not-found-state">
      <div class="not-found-icon">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
      </div>
      <h3 class="not-found-title">评估不存在</h3>
      <p class="not-found-desc">找不到该评估记录</p>
    </div>
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
.assessment-detail-page {
  max-width: 960px;
  margin: 0 auto;
  padding: 32px 24px;
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

/* Detail Header */
.detail-header {
  background: #fff;
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--radius-xl);
  padding: 28px 32px;
  margin-bottom: 20px;
  box-shadow: var(--shadow-sm);
}

.header-content {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 24px;
}

.detail-title {
  font-size: 22px;
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0 0 10px 0;
  letter-spacing: -0.02em;
}

.header-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.status-pill {
  display: inline-flex;
  align-items: center;
  padding: 3px 12px;
  border-radius: var(--radius-full);
  font-size: 12px;
  font-weight: 500;
  white-space: nowrap;
}

.meta-divider {
  width: 1px;
  height: 14px;
  background: var(--color-border);
}

.meta-text {
  font-size: 13px;
  color: var(--color-text-secondary);
}

.meta-date {
  color: var(--color-text-tertiary);
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
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

.btn-spinner {
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
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

/* Tab Bar */
.tab-bar {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px;
  background: var(--color-border-subtle);
  border-radius: var(--radius-lg);
  margin-bottom: 20px;
}

.tab-item {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 9px 18px;
  border: none;
  border-radius: var(--radius-md);
  background: transparent;
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.tab-item:hover {
  color: var(--color-text-primary);
  background: rgba(255, 255, 255, 0.6);
}

.tab-item.active {
  background: #fff;
  color: var(--color-accent);
  box-shadow: var(--shadow-sm);
}

/* Tab Content */
.tab-content {
  background: #fff;
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--radius-xl);
  padding: 28px 32px;
  box-shadow: var(--shadow-sm);
  min-height: 300px;
}

.tab-panel {
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Section Titles */
.section-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 16px 0;
  letter-spacing: -0.01em;
}

.chart-section {
  margin-bottom: 32px;
  padding-bottom: 32px;
  border-bottom: 1px solid var(--color-border-subtle);
}

.chart-wrapper {
  max-width: 480px;
  margin: 0 auto;
}

.report-section {
  margin-bottom: 0;
}

/* Markdown Content */
.markdown-content {
  font-size: 14px;
  line-height: 1.75;
  color: var(--color-text-primary);
}

.markdown-content :deep(h1),
.markdown-content :deep(h2),
.markdown-content :deep(h3) {
  color: var(--color-text-primary);
  margin-top: 24px;
  margin-bottom: 12px;
  font-weight: 600;
}

.markdown-content :deep(h1) { font-size: 20px; }
.markdown-content :deep(h2) { font-size: 17px; }
.markdown-content :deep(h3) { font-size: 15px; }

.markdown-content :deep(p) {
  margin: 0 0 12px 0;
}

.markdown-content :deep(ul),
.markdown-content :deep(ol) {
  padding-left: 20px;
  margin-bottom: 12px;
}

.markdown-content :deep(li) {
  margin-bottom: 4px;
}

.markdown-content :deep(strong) {
  color: var(--color-text-primary);
  font-weight: 600;
}

.markdown-content :deep(blockquote) {
  border-left: 3px solid var(--color-accent-subtle);
  padding-left: 16px;
  margin: 16px 0;
  color: var(--color-text-secondary);
}

/* Tab Empty State */
.tab-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
}

.tab-empty-icon {
  width: 72px;
  height: 72px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-accent-light);
  border-radius: var(--radius-full);
  margin-bottom: 16px;
  color: var(--color-accent);
}

.tab-empty-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 6px 0;
}

.tab-empty-desc {
  font-size: 13px;
  color: var(--color-text-tertiary);
  margin: 0;
}

/* Not Found State */
.not-found-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  text-align: center;
}

.not-found-icon {
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

.not-found-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 6px 0;
}

.not-found-desc {
  font-size: 14px;
  color: var(--color-text-tertiary);
  margin: 0;
}

/* Responsive */
@media (max-width: 768px) {
  .assessment-detail-page {
    padding: 20px 16px;
  }

  .detail-header {
    padding: 20px;
  }

  .header-content {
    flex-direction: column;
    gap: 16px;
  }

  .header-actions {
    width: 100%;
  }

  .header-actions .btn-primary,
  .header-actions .btn-secondary {
    flex: 1;
    justify-content: center;
  }

  .tab-bar {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }

  .tab-item {
    font-size: 12px;
    padding: 8px 14px;
  }

  .tab-content {
    padding: 20px;
  }

  .chart-wrapper {
    max-width: 100%;
  }
}
</style>
