<template>
  <div class="dashboard-page">
    <!-- Stats Cards -->
    <div class="stats-grid">
      <div class="stat-card" style="--delay: 0">
        <div class="stat-card__content">
          <div class="stat-card__number">{{ stats.classCount }}</div>
          <div class="stat-card__label">班级数</div>
        </div>
        <div class="stat-card__icon stat-card__icon--blue">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
        </div>
      </div>

      <div class="stat-card" style="--delay: 1">
        <div class="stat-card__content">
          <div class="stat-card__number">{{ stats.childCount }}</div>
          <div class="stat-card__label">幼儿数</div>
        </div>
        <div class="stat-card__icon stat-card__icon--green">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
        </div>
      </div>

      <div class="stat-card" style="--delay: 2">
        <div class="stat-card__content">
          <div class="stat-card__number">{{ stats.monthAnecdotes }}</div>
          <div class="stat-card__label">本月记录数</div>
        </div>
        <div class="stat-card__icon stat-card__icon--amber">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
        </div>
      </div>

      <div class="stat-card" style="--delay: 3">
        <div class="stat-card__content">
          <div class="stat-card__number">{{ stats.pendingAssessments }}</div>
          <div class="stat-card__label">待生成评估</div>
        </div>
        <div class="stat-card__icon stat-card__icon--violet">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="section-card">
      <div class="section-card__header">
        <h3 class="section-card__title">快捷操作</h3>
      </div>
      <div class="quick-actions">
        <router-link to="/anecdotes/new" class="quick-action-item">
          <div class="quick-action-item__icon quick-action-item__icon--blue">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
          </div>
          <span class="quick-action-item__label">新建观察记录</span>
        </router-link>
        <router-link to="/classes" class="quick-action-item">
          <div class="quick-action-item__icon quick-action-item__icon--green">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>
          </div>
          <span class="quick-action-item__label">管理班级</span>
        </router-link>
        <router-link to="/assessments" class="quick-action-item">
          <div class="quick-action-item__icon quick-action-item__icon--amber">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
          </div>
          <span class="quick-action-item__label">查看评估</span>
        </router-link>
        <router-link to="/compare" class="quick-action-item">
          <div class="quick-action-item__icon quick-action-item__icon--violet">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
          </div>
          <span class="quick-action-item__label">历史对比</span>
        </router-link>
      </div>
    </div>

    <!-- Recent Anecdotes -->
    <div class="section-card">
      <div class="section-card__header">
        <h3 class="section-card__title">最近观察记录</h3>
        <router-link to="/anecdotes" class="section-card__action">查看全部</router-link>
      </div>
      <div v-if="loading" class="loading-wrapper">
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
.dashboard-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--space-8) var(--space-6);
  display: flex;
  flex-direction: column;
  gap: var(--space-8);
}

/* ── Stats Grid ── */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-4);
}

.stat-card {
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--radius-xl);
  padding: var(--space-6);
  display: flex;
  align-items: center;
  justify-content: space-between;
  animation: fadeInUp 0.4s var(--transition-slow) both;
  animation-delay: calc(var(--delay) * 80ms);
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(12px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.stat-card__content {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.stat-card__number {
  font-size: 32px;
  font-weight: 700;
  line-height: 1.1;
  color: var(--color-text-primary);
  letter-spacing: -0.02em;
}

.stat-card__label {
  font-size: 14px;
  color: var(--color-text-secondary);
  font-weight: 400;
}

.stat-card__icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-card__icon--blue {
  background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%);
  color: #4F46E5;
}

.stat-card__icon--green {
  background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
  color: #059669;
}

.stat-card__icon--amber {
  background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
  color: #D97706;
}

.stat-card__icon--violet {
  background: linear-gradient(135deg, #F5F3FF 0%, #EDE9FE 100%);
  color: #7C3AED;
}

/* ── Section Card ── */
.section-card {
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--radius-xl);
  padding: var(--space-6);
}

.section-card__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-5);
}

.section-card__title {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
  letter-spacing: -0.01em;
}

.section-card__action {
  font-size: 13px;
  font-weight: 500;
  color: var(--color-accent);
  text-decoration: none;
  transition: color var(--transition-fast);
}

.section-card__action:hover {
  color: #3730A3;
}

/* ── Quick Actions ── */
.quick-actions {
  display: flex;
  gap: var(--space-3);
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
  padding-bottom: var(--space-1);
}

.quick-actions::-webkit-scrollbar {
  display: none;
}

.quick-action-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-lg);
  background: var(--color-bg-primary);
  border: 1px solid var(--color-border-subtle);
  text-decoration: none;
  white-space: nowrap;
  transition: border-color var(--transition-fast), box-shadow var(--transition-fast), transform var(--transition-fast);
  flex-shrink: 0;
}

.quick-action-item:hover {
  border-color: var(--color-accent);
  box-shadow: var(--shadow-sm);
  transform: translateY(-1px);
}

.quick-action-item:hover .quick-action-item__label {
  color: var(--color-accent);
}

.quick-action-item__icon {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: transform var(--transition-fast);
}

.quick-action-item:hover .quick-action-item__icon {
  transform: scale(1.05);
}

.quick-action-item__icon--blue {
  background: var(--color-accent-light);
  color: var(--color-accent);
}

.quick-action-item__icon--green {
  background: #ECFDF5;
  color: #059669;
}

.quick-action-item__icon--amber {
  background: #FFFBEB;
  color: #D97706;
}

.quick-action-item__icon--violet {
  background: #F5F3FF;
  color: #7C3AED;
}

.quick-action-item__label {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-primary);
  transition: color var(--transition-fast);
}

/* ── Anecdote List ── */
.anecdote-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.anecdote-list :deep(.anecdote-card) {
  border-left: 3px solid transparent;
  transition: border-left-color var(--transition-fast), background-color var(--transition-fast);
}

.anecdote-list :deep(.anecdote-card:hover) {
  border-left-color: var(--color-accent);
  background-color: var(--color-bg-primary);
}

/* ── Loading ── */
.loading-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-10);
}

/* ── Responsive ── */
@media (max-width: 1024px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .dashboard-page {
    padding: var(--space-4) var(--space-4);
    gap: var(--space-6);
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: var(--space-3);
  }

  .stat-card {
    padding: var(--space-4);
  }

  .stat-card__number {
    font-size: 26px;
  }

  .stat-card__icon {
    width: 40px;
    height: 40px;
  }

  .section-card {
    padding: var(--space-4);
  }

  .quick-actions {
    gap: var(--space-2);
  }

  .quick-action-item {
    padding: var(--space-3);
    flex-direction: column;
    align-items: center;
    text-align: center;
    min-width: 100px;
  }
}
</style>
