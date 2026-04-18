<template>
  <div class="page-container">
    <div class="page-header">
      <h2>{{ isEdit ? '编辑观察记录' : '新建观察记录' }}</h2>
      <div class="page-header-actions">
        <button class="btn btn-secondary" @click="$router.back()">取消</button>
        <button class="btn btn-primary" @click="handleSubmit" :disabled="!canSubmit || submitting">
          <span v-if="submitting" class="loading-spinner" style="width:14px;height:14px;border-width:2px;"></span>
          {{ isEdit ? '保存修改' : '提交记录' }}
        </button>
      </div>
    </div>

    <div class="split-panel">
      <!-- Form -->
      <div class="form-panel">
        <AnecdoteForm
          :form="form"
          :classes="classes"
          :recognized-names="recognizedNames"
          :is-recognizing="isRecognizing"
          @content-change="recognizeNamesDebounced"
          @add-name="addName"
          @remove-name="removeName"
        />
      </div>

      <!-- Preview -->
      <div class="preview-panel">
        <div class="preview-panel-header">
          <h3>预览</h3>
        </div>
        <div v-if="hasContent" class="preview-content">
          <div class="preview-meta">
            <span v-if="form.class_id" class="preview-badge preview-badge--class">{{ currentClassName }}</span>
            <span v-if="form.location" class="preview-badge preview-badge--location">
              <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
              {{ form.location }}
            </span>
            <span v-if="form.activity_type" class="preview-badge preview-badge--activity">{{ form.activity_type }}</span>
          </div>
          <div class="preview-time" v-if="form.observation_time">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            {{ formatDate(form.observation_time) }}
          </div>
          <div class="preview-body">
            <p>{{ form.content }}</p>
          </div>
          <div class="preview-names" v-if="form.children_names.length">
            <span class="preview-label">关联幼儿</span>
            <div class="preview-tag-group">
              <NameTag
                v-for="name in form.children_names"
                :key="name"
                :name="name"
              />
            </div>
          </div>
          <div class="preview-teacher" v-if="form.teacher_name">
            <span class="preview-label">教师</span>
            <span class="preview-teacher-name">{{ form.teacher_name }}</span>
          </div>
        </div>
        <div v-else class="preview-empty">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
          <p>填写左侧表单，预览将在此显示</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAnecdote } from '../composables/useAnecdote.js'
import { useClassStore } from '../stores/classes.js'
import { useToast } from '../composables/useToast.js'
import AnecdoteForm from '../components/anecdote/AnecdoteForm.vue'
import NameTag from '../components/anecdote/NameTag.vue'
import { formatDate, getCurrentDateTime } from '../utils/format.js'

const route = useRoute()
const router = useRouter()
const classStore = useClassStore()
const toast = useToast()

const isEdit = computed(() => !!route.params.id)
const {
  form,
  recognizedNames,
  isRecognizing,
  recognizeNamesDebounced,
  addName,
  removeName,
  resetForm,
  loadAnecdote,
  submitForm
} = useAnecdote()

const classes = ref([])
const submitting = ref(false)

const currentClassName = computed(() => {
  const cls = classes.value.find(c => c.id == form.value.class_id)
  return cls?.name || ''
})

const canSubmit = computed(() => {
  return form.value.class_id && form.value.content && form.value.content.length >= 20
})

const hasContent = computed(() => {
  return form.value.content || form.value.location || form.value.class_id
})

onMounted(async () => {
  // Set default time
  form.value.observation_time = getCurrentDateTime()

  // Load classes
  try {
    await classStore.fetchClasses()
    classes.value = classStore.classes
  } catch {
    // Silent fail
  }

  // If editing, load existing anecdote
  if (isEdit.value) {
    try {
      const { useAnecdoteStore } = await import('../stores/anecdotes.js')
      const store = useAnecdoteStore()
      const anecdote = await store.fetchAnecdoteById(route.params.id)
      loadAnecdote(anecdote)
    } catch {
      toast.error('加载记录失败')
    }
  }
})

async function handleSubmit() {
  if (!canSubmit.value) return
  submitting.value = true
  try {
    await submitForm(isEdit.value)
    toast.success(isEdit.value ? '记录已更新' : '记录已提交')
    router.push('/anecdotes')
  } catch {
    // Error handled by interceptor
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
/* Split Panel */
.split-panel {
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: 32px;
  align-items: start;
}

/* Form Panel */
.form-panel {
  min-width: 0;
}

/* Preview Panel */
.preview-panel {
  position: sticky;
  top: 24px;
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: 24px;
  box-shadow: var(--shadow-sm);
}

.preview-panel-header {
  margin-bottom: 20px;
  padding-bottom: 14px;
  border-bottom: 1px solid var(--color-border);
}

.preview-panel-header h3 {
  font-size: var(--font-size-sm);
  font-weight: 600;
  color: var(--color-text-primary);
}

.preview-meta {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 16px;
}

.preview-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px 12px;
  border-radius: var(--radius-full);
  font-size: var(--font-size-xs);
  font-weight: 500;
}

.preview-badge--class {
  background: var(--color-accent-light);
  color: var(--color-accent);
}

.preview-badge--location {
  background: var(--color-bg-primary);
  color: var(--color-text-secondary);
  border: 1px solid var(--color-border);
}

.preview-badge--activity {
  background: #ECFDF5;
  color: #059669;
}

.preview-time {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
  margin-bottom: 16px;
}

.preview-body {
  font-size: var(--font-size-sm);
  line-height: 1.8;
  color: var(--color-text-primary);
  white-space: pre-wrap;
  margin-bottom: 20px;
  padding: 16px;
  background: var(--color-bg-primary);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border);
}

.preview-names {
  margin-bottom: 16px;
}

.preview-label {
  display: block;
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
  margin-bottom: 8px;
  font-weight: 500;
}

.preview-tag-group {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.preview-teacher {
  padding-top: 14px;
  border-top: 1px solid var(--color-border);
}

.preview-teacher-name {
  font-size: var(--font-size-sm);
  color: var(--color-text-primary);
  font-weight: 500;
}

.preview-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 240px;
  text-align: center;
  color: var(--color-text-tertiary);
  gap: 12px;
}

.preview-empty svg {
  opacity: 0.3;
}

.preview-empty p {
  font-size: var(--font-size-sm);
}

/* Responsive */
@media (max-width: 1024px) {
  .split-panel {
    grid-template-columns: 1fr;
    gap: 24px;
  }

  .preview-panel {
    position: static;
    order: -1;
  }
}

@media (max-width: 640px) {
  .preview-panel {
    padding: 18px;
    border-radius: var(--radius-lg);
  }

  .preview-body {
    padding: 12px;
  }
}
</style>
