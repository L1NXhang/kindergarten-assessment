<template>
  <div
    class="uploader"
    :class="{ 'uploader--dragover': isDragover }"
    @click="triggerUpload"
    @dragover.prevent="onDragOver"
    @dragleave="onDragLeave"
    @drop.prevent="onDrop"
  >
    <input
      ref="fileInput"
      type="file"
      :accept="accept"
      class="uploader-input"
      @change="onFileChange"
    />

    <div class="uploader-icon">
      <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
    </div>

    <p class="uploader-text">{{ isDragover ? '释放文件以上传' : '点击或拖拽文件到此处' }}</p>
    <p class="uploader-hint">支持 .xlsx, .xls 格式</p>

    <div v-if="uploading" class="uploader-progress">
      <div class="uploader-progress-track">
        <div class="uploader-progress-fill" :style="{ width: progress + '%' }"></div>
      </div>
      <p class="uploader-progress-label">上传中... {{ progress }}%</p>
    </div>

    <div v-if="uploadedFile" class="uploader-result">
      <span class="uploader-result-icon">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
      </span>
      <span class="uploader-result-name">{{ uploadedFile.name }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  accept: { type: String, default: '.xlsx,.xls' }
})

const emit = defineEmits(['upload', 'uploaded'])

const fileInput = ref(null)
const isDragover = ref(false)
const uploading = ref(false)
const progress = ref(0)
const uploadedFile = ref(null)

function triggerUpload() {
  fileInput.value?.click()
}

function onDragOver() {
  isDragover.value = true
}

function onDragLeave() {
  isDragover.value = false
}

function onDrop(e) {
  isDragover.value = false
  const files = e.dataTransfer.files
  if (files.length > 0) {
    handleFile(files[0])
  }
}

function onFileChange(e) {
  const files = e.target.files
  if (files.length > 0) {
    handleFile(files[0])
  }
}

function handleFile(file) {
  const validTypes = [
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/vnd.ms-excel'
  ]
  const ext = file.name.split('.').pop().toLowerCase()
  if (!validTypes.includes(file.type) && !['xlsx', 'xls'].includes(ext)) {
    emit('upload', { error: '请上传 Excel 文件 (.xlsx 或 .xls)' })
    return
  }

  emit('upload', { file })
  uploading.value = true
  progress.value = 0

  // Simulate upload progress
  const interval = setInterval(() => {
    progress.value += 10
    if (progress.value >= 100) {
      clearInterval(interval)
      uploading.value = false
      uploadedFile.value = file
      emit('uploaded', file)
    }
  }, 100)
}

function reset() {
  uploadedFile.value = null
  progress.value = 0
  uploading.value = false
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

defineExpose({ reset })
</script>

<style scoped>
.uploader-input {
  display: none;
}

.uploader {
  border: 2px dashed var(--color-border);
  border-radius: var(--radius-xl);
  padding: 40px 24px;
  text-align: center;
  cursor: pointer;
  transition: all var(--transition-normal);
  background: #FDFCFA;
}

.uploader:hover {
  border-color: var(--color-text-tertiary);
  background: #FAF9F7;
}

.uploader--dragover {
  border-color: var(--color-accent);
  background: var(--color-accent-light);
}

.uploader-icon {
  color: var(--color-text-tertiary);
  margin-bottom: 14px;
  transition: color var(--transition-fast);
}

.uploader--dragover .uploader-icon {
  color: var(--color-accent);
}

.uploader-text {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-secondary);
  margin: 0 0 6px 0;
}

.uploader-hint {
  font-size: 12px;
  color: var(--color-text-tertiary);
  margin: 0;
}

/* Progress */
.uploader-progress {
  margin-top: 20px;
  max-width: 280px;
  margin-left: auto;
  margin-right: auto;
}

.uploader-progress-track {
  height: 6px;
  background: var(--color-border-subtle);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.uploader-progress-fill {
  height: 100%;
  background: var(--color-accent);
  border-radius: var(--radius-full);
  transition: width 150ms ease;
}

.uploader-progress-label {
  font-size: 12px;
  color: var(--color-text-tertiary);
  margin: 8px 0 0 0;
}

/* Result */
.uploader-result {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin-top: 16px;
  padding: 6px 14px;
  background: #ECFDF5;
  border-radius: var(--radius-full);
}

.uploader-result-icon {
  color: #059669;
  display: flex;
  align-items: center;
}

.uploader-result-name {
  font-size: 13px;
  color: #065F46;
  font-weight: 500;
}
</style>
