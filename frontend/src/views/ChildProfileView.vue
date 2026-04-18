<template>
  <div class="page-container">
    <!-- Child Info -->
    <div class="child-profile-header card mb-lg" v-if="child">
      <div class="child-profile-info">
        <div class="child-avatar" :style="{ background: avatarColor }">
          {{ avatarText }}
        </div>
        <div class="child-details">
          <h2 class="child-name">{{ child.name }}</h2>
          <div class="child-meta">
            <span v-if="child.gender">{{ child.gender === 'male' ? '男' : '女' }}</span>
            <span v-if="child.birthday">{{ calcAge(child.birthday) }}</span>
            <span v-if="child.class_name" class="badge badge-info">{{ child.class_name }}</span>
          </div>
        </div>
      </div>
      <div class="child-stats">
        <div class="child-stat-item">
          <span class="child-stat-value">{{ child.anecdote_count || 0 }}</span>
          <span class="child-stat-label">观察记录</span>
        </div>
        <div class="child-stat-item">
          <span class="child-stat-value">{{ child.assessment_count || 0 }}</span>
          <span class="child-stat-label">评估报告</span>
        </div>
      </div>
    </div>

    <!-- Domain Radar -->
    <div class="grid grid-2 mb-lg" v-if="child?.latest_scores">
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">发展领域评估</h3>
        </div>
        <DomainRadar :scores="child.latest_scores" :height="280" />
      </div>
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">各领域得分</h3>
        </div>
        <div class="domain-scores">
          <div v-for="domain in domains" :key="domain.key" class="domain-score-item">
            <div class="domain-score-header">
              <span class="domain-dot" :style="{ background: domain.color }"></span>
              <span class="domain-name">{{ domain.name }}</span>
              <span class="domain-value">{{ child.latest_scores[domain.key] || '-' }}</span>
            </div>
            <div class="domain-bar">
              <div
                class="domain-bar-fill"
                :style="{ width: ((child.latest_scores[domain.key] || 0) / 5 * 100) + '%', background: domain.color }"
              ></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Anecdote Timeline -->
    <div class="card">
      <div class="card-header">
        <h3 class="card-title">观察记录</h3>
        <router-link to="/anecdotes/new" class="btn btn-ghost btn-sm">新建记录</router-link>
      </div>
      <AnecdoteTimeline :anecdotes="anecdotes" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useChildStore } from '../stores/children.js'
import { useAnecdoteStore } from '../stores/anecdotes.js'
import { useToast } from '../composables/useToast.js'
import DomainRadar from '../components/assessment/DomainRadar.vue'
import AnecdoteTimeline from '../components/anecdote/AnecdoteTimeline.vue'
import { DOMAINS } from '../utils/constants.js'
import { calcAge } from '../utils/format.js'

const route = useRoute()
const childStore = useChildStore()
const anecdoteStore = useAnecdoteStore()
const toast = useToast()

const childId = route.params.id
const child = ref(null)
const anecdotes = ref([])
const domains = DOMAINS

const avatarText = computed(() => (child.value?.name || '?').slice(-1))
const avatarColor = computed(() => {
  const colors = ['#3B82F6', '#10B981', '#F59E0B', '#8B5CF6', '#EC4899']
  const index = (child.value?.name || '').charCodeAt(0) % colors.length
  return colors[index]
})

onMounted(async () => {
  try {
    child.value = await childStore.fetchChildById(childId)
    const childAnecdotes = await import('../api/children.js').then(m => m.getChildAnecdotes(childId))
    anecdotes.value = childAnecdotes || []
  } catch {
    toast.error('加载幼儿信息失败')
  }
})
</script>

<style scoped>
.child-profile-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.child-profile-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.child-avatar {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: var(--font-size-xl);
  font-weight: 700;
}

.child-name {
  font-size: var(--font-size-2xl);
  font-weight: 700;
  color: var(--color-text-primary);
  margin-bottom: 4px;
}

.child-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
}

.child-stats {
  display: flex;
  gap: 24px;
}

.child-stat-item {
  text-align: center;
}

.child-stat-value {
  display: block;
  font-size: var(--font-size-2xl);
  font-weight: 700;
  color: var(--color-text-primary);
}

.child-stat-label {
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
}

.domain-scores {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 8px 0;
}

.domain-score-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
}

.domain-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.domain-name {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  flex: 1;
}

.domain-value {
  font-size: var(--font-size-sm);
  font-weight: 600;
  color: var(--color-text-primary);
}

.domain-bar {
  height: 6px;
  background: var(--color-bg-tertiary);
  border-radius: 3px;
  overflow: hidden;
}

.domain-bar-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.5s ease;
}
</style>
