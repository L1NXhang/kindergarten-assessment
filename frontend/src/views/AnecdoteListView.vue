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
      <select v-model="filters.class_id" class="form-select" @change="handleFilter">
        <option value="">全部班级</option>
        <option v-for="cls in classes" :key="cls.id" :value="cls.id">{{ cls.name }}</option>
      </select>
      <input
        type="date"
        v-model="filters.date_from"
        class="form-input"
        placeholder="开始日期"
        @change="handleFilter"
      />
      <span class="text-tertiary">至</span>
      <input
        type="date"
        v-model="filters.date_to"
        class="form-input"
        placeholder="结束日期"
        @change="handleFilter"
      />
      <input
        v-model="filters.child_name"
        class="form-input"
        placeholder="搜索幼儿姓名"
        @keyup.enter="handleFilter"
      />
      <button class="btn btn-secondary btn-sm" @click="resetFilters">重置</button>
    </div>

    <!-- List -->
    <div v-if="loading" class="flex-center" style="padding:60px;">
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
          <button class="btn btn-ghost btn-sm" @click.stop="handleDelete(item)">删除</button>
        </template>
      </AnecdoteCard>
    </div>

    <EmptyState v-else title="暂无观察记录" description="调整筛选条件或新建一条观察记录">
      <template #action>
        <router-link to="/anecdotes/new" class="btn btn-primary">新建记录</router-link>
      </template>
    </EmptyState>

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
.anecdote-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
</style>
