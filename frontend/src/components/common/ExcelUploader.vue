<template>
  <div
    class="upload-area"
    :class="{ dragover: isDragover }"
    @click="triggerUpload"
    @dragover.prevent="onDragOver"
    @dragleave="onDragLeave"
    @drop.prevent="onDrop"
  >
    <input
      ref="fileInput"
      type="file"
      :accept="accept"
      class="upload-input"
      @change="onFileChange"
    />
    <div class="upload-area-icon">
      <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
    </div>
    <p class="upload-area-text">{{ isDragover ? '释放文件以上传' : '点击或拖拽文件到此处' }}</p>
    <p class="upload-area-hint">支持 .xlsx, .xls 格式</p>

    <div v-if="uploading" class="upload-progress mt-md">
      <div class="progress-bar">
        <div class="progress-bar-fill" :style="{ width: progress + '%' }"></div>
      </div>
      <p class="text-xs text-tertiary mt-sm">上传中... {{ progress }}%</p>
    </div>

    <div v-if="uploadedFile" class="upload-result mt-sm">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
      <span class="text-sm">{{ uploadedFile.name }}</span>
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
.upload-input {
  display: none;
}

.upload-area {
  border: 2px dashed var(--color-border);
  border-radius: var(--radius-lg);
  padding: 40px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.upload-area:hover,
.upload-area.dragover {
  border-color: var(--color-accent);
  background: var(--color-accent-light);
}

.upload-area-icon {
  color: var(--color-text-tertiary);
  margin-bottom: 12px;
}

.upload-area-text {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
}

.upload-area-hint {
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
  margin-top: 4px;
}

.upload-result {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--color-success);
}
</style>
