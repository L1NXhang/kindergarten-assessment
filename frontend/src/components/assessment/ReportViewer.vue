<template>
  <div class="report-viewer">
    <!-- Loading State -->
    <div v-if="loading" class="report-loading">
      <div class="report-spinner"></div>
      <span class="report-loading-text">加载中...</span>
    </div>

    <!-- Content -->
    <div v-else-if="content" class="markdown-content" v-html="renderedContent"></div>

    <!-- Empty State -->
    <div v-else class="report-empty">
      <div class="report-empty-icon">
        <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
      </div>
      <h3 class="report-empty-title">暂无报告内容</h3>
      <p class="report-empty-desc">评估报告尚未生成</p>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

const props = defineProps({
  content: { type: String, default: '' },
  loading: { type: Boolean, default: false }
})

const renderedContent = computed(() => {
  if (!props.content) return ''
  const html = marked(props.content)
  return DOMPurify.sanitize(html)
})
</script>

<style scoped>
/* Loading State */
.report-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px 20px;
  gap: 12px;
}

.report-spinner {
  width: 28px;
  height: 28px;
  border: 3px solid var(--color-border);
  border-top-color: var(--color-accent);
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.report-loading-text {
  font-size: 13px;
  color: var(--color-text-tertiary);
}

/* Markdown Content */
.markdown-content {
  font-size: 14px;
  line-height: 1.8;
  color: var(--color-text-primary);
}

.markdown-content :deep(h1),
.markdown-content :deep(h2),
.markdown-content :deep(h3) {
  color: var(--color-text-primary);
  margin-top: 28px;
  margin-bottom: 12px;
  font-weight: 600;
  letter-spacing: -0.01em;
}

.markdown-content :deep(h1) { font-size: 20px; }
.markdown-content :deep(h2) { font-size: 17px; }
.markdown-content :deep(h3) { font-size: 15px; }

.markdown-content :deep(h1:first-child),
.markdown-content :deep(h2:first-child),
.markdown-content :deep(h3:first-child) {
  margin-top: 0;
}

.markdown-content :deep(p) {
  margin: 0 0 14px 0;
}

.markdown-content :deep(p:last-child) {
  margin-bottom: 0;
}

.markdown-content :deep(ul),
.markdown-content :deep(ol) {
  padding-left: 22px;
  margin-bottom: 14px;
}

.markdown-content :deep(li) {
  margin-bottom: 6px;
  line-height: 1.7;
}

.markdown-content :deep(li:last-child) {
  margin-bottom: 0;
}

.markdown-content :deep(strong) {
  color: var(--color-text-primary);
  font-weight: 600;
}

.markdown-content :deep(em) {
  color: var(--color-text-secondary);
}

.markdown-content :deep(blockquote) {
  border-left: 3px solid var(--color-accent-subtle);
  padding: 4px 0 4px 16px;
  margin: 16px 0;
  color: var(--color-text-secondary);
  background: var(--color-accent-light);
  border-radius: 0 var(--radius-md) var(--radius-md) 0;
  padding-right: 16px;
}

.markdown-content :deep(code) {
  background: var(--color-border-subtle);
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 13px;
  color: var(--color-text-primary);
}

.markdown-content :deep(pre) {
  background: var(--color-border-subtle);
  padding: 16px;
  border-radius: var(--radius-md);
  overflow-x: auto;
  margin: 16px 0;
}

.markdown-content :deep(pre code) {
  background: none;
  padding: 0;
  font-size: 13px;
}

.markdown-content :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 16px 0;
  font-size: 13px;
}

.markdown-content :deep(th),
.markdown-content :deep(td) {
  padding: 10px 14px;
  text-align: left;
  border-bottom: 1px solid var(--color-border-subtle);
}

.markdown-content :deep(th) {
  font-weight: 600;
  color: var(--color-text-primary);
  background: var(--color-border-subtle);
}

.markdown-content :deep(hr) {
  border: none;
  border-top: 1px solid var(--color-border-subtle);
  margin: 24px 0;
}

/* Empty State */
.report-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px 20px;
  text-align: center;
}

.report-empty-icon {
  width: 64px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-accent-light);
  border-radius: var(--radius-full);
  margin-bottom: 14px;
  color: var(--color-accent);
}

.report-empty-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 4px 0;
}

.report-empty-desc {
  font-size: 13px;
  color: var(--color-text-tertiary);
  margin: 0;
}
</style>
