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
        <h3>预览</h3>
        <div v-if="hasContent" class="preview-content">
          <div class="preview-meta">
            <span v-if="form.class_id" class="badge badge-info">{{ currentClassName }}</span>
            <span v-if="form.location" class="badge badge-neutral">{{ form.location }}</span>
            <span v-if="form.activity_type" class="badge badge-neutral">{{ form.activity_type }}</span>
          </div>
          <div class="preview-time mt-sm" v-if="form.observation_time">
            {{ formatDate(form.observation_time) }}
          </div>
          <div class="preview-body mt-md">
            <p>{{ form.content }}</p>
          </div>
          <div class="preview-names mt-md" v-if="form.children_names.length">
            <span class="text-xs text-tertiary">关联幼儿：</span>
            <div class="tag-group mt-sm">
              <NameTag
                v-for="name in form.children_names"
                :key="name"
                :name="name"
              />
            </div>
          </div>
          <div class="preview-teacher mt-md" v-if="form.teacher_name">
            <span class="text-xs text-tertiary">教师：{{ form.teacher_name }}</span>
          </div>
        </div>
        <div v-else class="preview-empty">
          <p class="text-tertiary text-sm">填写左侧表单，预览将在此显示</p>
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
.form-panel {
  min-width: 0;
}

.preview-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 200px;
}

.preview-meta {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.preview-time {
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
}

.preview-body {
  font-size: var(--font-size-sm);
  line-height: 1.8;
  color: var(--color-text-primary);
  white-space: pre-wrap;
}
</style>
