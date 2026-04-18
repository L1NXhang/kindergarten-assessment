<template>
  <div class="page-container">
    <!-- Stats Cards -->
    <div class="grid grid-4 mb-lg">
      <div class="stat-card">
        <div class="flex-between mb-sm">
          <div>
            <div class="stat-card-value">{{ stats.classCount }}</div>
            <div class="stat-card-label">班级数</div>
          </div>
          <div class="stat-card-icon" style="background:#EFF6FF;color:#2563EB;">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
          </div>
        </div>
      </div>

      <div class="stat-card">
        <div class="flex-between mb-sm">
          <div>
            <div class="stat-card-value">{{ stats.childCount }}</div>
            <div class="stat-card-label">幼儿数</div>
          </div>
          <div class="stat-card-icon" style="background:#ECFDF5;color:#10B981;">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
          </div>
        </div>
      </div>

      <div class="stat-card">
        <div class="flex-between mb-sm">
          <div>
            <div class="stat-card-value">{{ stats.monthAnecdotes }}</div>
            <div class="stat-card-label">本月记录数</div>
          </div>
          <div class="stat-card-icon" style="background:#FFF7ED;color:#D97706;">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
          </div>
        </div>
      </div>

      <div class="stat-card">
        <div class="flex-between mb-sm">
          <div>
            <div class="stat-card-value">{{ stats.pendingAssessments }}</div>
            <div class="stat-card-label">待生成评估</div>
          </div>
          <div class="stat-card-icon" style="background:#F5F3FF;color:#8B5CF6;">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="card mb-lg">
      <div class="card-header">
        <h3 class="card-title">快捷操作</h3>
      </div>
      <div class="quick-actions">
        <router-link to="/anecdotes/new" class="quick-action-item">
          <div class="quick-action-icon" style="background:#EFF6FF;color:#2563EB;">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
          </div>
          <span>新建观察记录</span>
        </router-link>
        <router-link to="/classes" class="quick-action-item">
          <div class="quick-action-icon" style="background:#ECFDF5;color:#10B981;">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>
          </div>
          <span>管理班级</span>
        </router-link>
        <router-link to="/assessments" class="quick-action-item">
          <div class="quick-action-icon" style="background:#FFF7ED;color:#D97706;">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
          </div>
          <span>查看评估</span>
        </router-link>
        <router-link to="/compare" class="quick-action-item">
          <div class="quick-action-icon" style="background:#F5F3FF;color:#8B5CF6;">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
          </div>
          <span>历史对比</span>
        </router-link>
      </div>
    </div>

    <!-- Recent Anecdotes -->
    <div class="card">
      <div class="card-header">
        <h3 class="card-title">最近观察记录</h3>
        <router-link to="/anecdotes" class="btn btn-ghost btn-sm">查看全部</router-link>
      </div>
      <div v-if="loading" class="flex-center" style="padding:40px;">
        <span class="loading-spinner"></span>
      </div>
      <div v-else-if="recentAnecdotes.length > 0" class="anecdote-list">
        <AnecdoteCard
          v-for="item in recentAnecdotes"
          :key="item.id"
          :anecdote="item"
          @click="$router.push(`/anecdotes/${item.id}/edit`)"
        />
      </div>
      <EmptyState v-else title="暂无观察记录" description="点击上方「新建观察记录」开始记录幼儿的发展情况">
        <template #action>
          <router-link to="/anecdotes/new" class="btn btn-primary">新建记录</router-link>
        </template>
      </EmptyState>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AnecdoteCard from '../components/anecdote/AnecdoteCard.vue'
import EmptyState from '../components/common/EmptyState.vue'
import { useAnecdoteStore } from '../stores/anecdotes.js'
import { useClassStore } from '../stores/classes.js'
import { useChildStore } from '../stores/children.js'
import { useAssessmentStore } from '../stores/assessments.js'
import { getDashboardStats } from '../api/reports.js'

const anecdoteStore = useAnecdoteStore()
const classStore = useClassStore()
const childStore = useChildStore()
const assessmentStore = useAssessmentStore()

const loading = ref(false)
const recentAnecdotes = ref([])
const stats = ref({
  classCount: 0,
  childCount: 0,
  monthAnecdotes: 0,
  pendingAssessments: 0
})

onMounted(async () => {
  loading.value = true
  try {
    await Promise.all([
      classStore.fetchClasses(),
      anecdoteStore.fetchAnecdotes({ limit: 10 }),
      assessmentStore.fetchAssessments({ status: 'pending' })
    ])

    recentAnecdotes.value = anecdoteStore.anecdotes.slice(0, 10)

    try {
      const dashboardData = await getDashboardStats()
      stats.value = {
        classCount: dashboardData.class_count || classStore.classes.length,
        childCount: dashboardData.child_count || 0,
        monthAnecdotes: dashboardData.month_anecdotes || anecdoteStore.total,
        pendingAssessments: dashboardData.pending_assessments || assessmentStore.assessments.length
      }
    } catch {
      stats.value = {
        classCount: classStore.classes.length,
        childCount: 0,
        monthAnecdotes: anecdoteStore.total,
        pendingAssessments: assessmentStore.assessments.length
      }
    }
  } catch {
    // Silently handle
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.quick-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.quick-action-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  border-radius: var(--radius-lg);
  background: var(--color-bg-tertiary);
  border: 1px solid var(--color-border);
  font-size: var(--font-size-sm);
  font-weight: 500;
  color: var(--color-text-primary);
  text-decoration: none;
  transition: all 0.15s ease;
}

.quick-action-item:hover {
  border-color: var(--color-accent);
  background: var(--color-accent-light);
  color: var(--color-accent);
}

.quick-action-icon {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.anecdote-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
</style>
