<template>
  <div class="page-container">
    <div class="page-header">
      <h2>观察记录</h2>
      <div class="page-header-actions">
        <router-link to="/anecdotes/new" class="btn btn-primary">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
          新建记录
        </router-link>
      </div>
    </div>

    <!-- Filters -->
    <div class="filter-bar">
      <div class="filter-pills">
        <div class="filter-pill">
          <select v-model="filters.class_id" class="filter-select" @change="handleFilter">
            <option value="">全部班级</option>
            <option v-for="cls in classes" :key="cls.id" :value="cls.id">{{ cls.name }}</option>
          </select>
        </div>
        <div class="filter-pill filter-pill--date">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
          <input
            type="date"
            v-model="filters.date_from"
            class="filter-date-input"
            @change="handleFilter"
          />
          <span class="filter-date-sep">至</span>
          <input
            type="date"
            v-model="filters.date_to"
            class="filter-date-input"
            @change="handleFilter"
          />
        </div>
        <div class="filter-pill filter-pill--search">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
          <input
            v-model="filters.child_name"
            class="filter-search-input"
            placeholder="搜索幼儿姓名"
            @keyup.enter="handleFilter"
          />
        </div>
        <button class="filter-reset" @click="resetFilters">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"/></svg>
          重置
        </button>
      </div>
    </div>

    <!-- List -->
    <div v-if="loading" class="loading-container">
      <span class="loading-spinner"></span>
    </div>

    <div v-else-if="anecdotes.length > 0" class="anecdote-list">
      <AnecdoteCard
        v-for="item in anecdotes"
        :key="item.id"
        :anecdote="item"
        :show-actions="true"
        @click="$router.push(`/anecdotes/${item.id}/edit`)"
      >
        <template #actions>
          <button class="card-delete-btn" @click.stop="handleDelete(item)">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
          </button>
        </template>
      </AnecdoteCard>
    </div>

    <div v-else class="empty-state">
      <div class="empty-state-icon">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
      </div>
      <h3 class="empty-state-title">暂无观察记录</h3>
      <p class="empty-state-desc">调整筛选条件或新建一条观察记录</p>
      <router-link to="/anecdotes/new" class="btn btn-primary btn-sm">新建记录</router-link>
    </div>

    <ConfirmDialog
      v-model="showDeleteConfirm"
      title="删除记录"
      message="确定要删除这条观察记录吗？此操作不可恢复。"
      confirm-text="删除"
      type="danger"
      @confirm="confirmDelete"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useAnecdoteStore } from '../stores/anecdotes.js'
import { useClassStore } from '../stores/classes.js'
import { useToast } from '../composables/useToast.js'
import AnecdoteCard from '../components/anecdote/AnecdoteCard.vue'
import EmptyState from '../components/common/EmptyState.vue'
import ConfirmDialog from '../components/common/ConfirmDialog.vue'

const anecdoteStore = useAnecdoteStore()
const classStore = useClassStore()
const toast = useToast()

const loading = ref(false)
const anecdotes = ref([])
const classes = ref([])
const showDeleteConfirm = ref(false)
const deletingItem = ref(null)

const filters = reactive({
  class_id: '',
  date_from: '',
  date_to: '',
  child_name: ''
})

onMounted(async () => {
  loading.value = true
  try {
    await Promise.all([
      classStore.fetchClasses(),
      anecdoteStore.fetchAnecdotes()
    ])
    classes.value = classStore.classes
    anecdotes.value = anecdoteStore.anecdotes
  } catch {
    toast.error('加载失败')
  } finally {
    loading.value = false
  }
})

function handleFilter() {
  loading.value = true
  anecdoteStore.fetchAnecdotes({ ...filters }).then(() => {
    anecdotes.value = anecdoteStore.anecdotes
  }).finally(() => {
    loading.value = false
  })
}

function resetFilters() {
  filters.class_id = ''
  filters.date_from = ''
  filters.date_to = ''
  filters.child_name = ''
  handleFilter()
}

function handleDelete(item) {
  deletingItem.value = item
  showDeleteConfirm.value = true
}

async function confirmDelete() {
  if (!deletingItem.value) return
  try {
    await anecdoteStore.removeAnecdote(deletingItem.value.id)
    anecdotes.value = anecdoteStore.anecdotes
    toast.success('记录已删除')
  } catch {
    // Error handled by interceptor
  }
}
</script>

<style scoped>
/* Filter Bar */
.filter-bar {
  margin-bottom: 24px;
}

.filter-pills {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.filter-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-full);
  padding: 6px 14px;
  transition: all var(--transition-fast);
  color: var(--color-text-secondary);
}

.filter-pill:focus-within {
  border-color: var(--color-accent);
  box-shadow: 0 0 0 3px var(--color-accent-light);
}

.filter-select {
  border: none;
  background: transparent;
  font-size: var(--font-size-sm);
  color: var(--color-text-primary);
  outline: none;
  cursor: pointer;
  padding: 0;
  appearance: none;
  -webkit-appearance: none;
  min-width: 100px;
}

.filter-date-input {
  border: none;
  background: transparent;
  font-size: var(--font-size-sm);
  color: var(--color-text-primary);
  outline: none;
  padding: 0;
  width: 130px;
  color-scheme: light;
}

.filter-date-sep {
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
}

.filter-search-input {
  border: none;
  background: transparent;
  font-size: var(--font-size-sm);
  color: var(--color-text-primary);
  outline: none;
  padding: 0;
  width: 160px;
}

.filter-search-input::placeholder {
  color: var(--color-text-tertiary);
}

.filter-reset {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 6px 14px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-full);
  background: var(--color-bg-secondary);
  color: var(--color-text-secondary);
  font-size: var(--font-size-sm);
  cursor: pointer;
  transition: all var(--transition-fast);
  white-space: nowrap;
}

.filter-reset:hover {
  border-color: var(--color-accent);
  color: var(--color-accent);
  background: var(--color-accent-light);
}

/* Loading */
.loading-container {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 60px;
}

/* Anecdote List */
.anecdote-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* Card Delete Button */
.card-delete-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: var(--radius-full);
  border: none;
  background: transparent;
  color: var(--color-text-tertiary);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.card-delete-btn:hover {
  background: #FEF2F2;
  color: #DC2626;
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 64px 24px;
  text-align: center;
}

.empty-state-icon {
  color: var(--color-text-tertiary);
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-state-title {
  font-size: var(--font-size-base);
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: 6px;
}

.empty-state-desc {
  font-size: var(--font-size-sm);
  color: var(--color-text-tertiary);
  margin-bottom: 20px;
}

/* Responsive */
@media (max-width: 768px) {
  .filter-pills {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-pill {
    width: 100%;
    justify-content: flex-start;
  }

  .filter-select {
    flex: 1;
  }

  .filter-date-input {
    flex: 1;
    width: auto;
  }

  .filter-search-input {
    flex: 1;
    width: auto;
  }

  .filter-reset {
    justify-content: center;
  }
}
</style>
