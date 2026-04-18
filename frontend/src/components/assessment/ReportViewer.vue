<template>
  <div class="report-viewer">
    <div v-if="loading" class="report-loading">
      <span class="loading-spinner"></span>
      <span class="text-sm text-secondary">加载中...</span>
    </div>
    <div v-else-if="content" class="markdown-content" v-html="renderedContent"></div>
    <EmptyState v-else title="暂无报告内容" description="评估报告尚未生成" />
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
.report-loading {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 40px;
  justify-content: center;
}
</style>
