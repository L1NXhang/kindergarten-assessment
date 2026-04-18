<template>
  <div class="profile-page">
    <!-- Profile Header -->
    <div class="profile-header" v-if="child">
      <div class="profile-header__main">
        <div class="profile-avatar" :style="{ background: avatarColor }">
          {{ avatarText }}
        </div>
        <div class="profile-identity">
          <h1 class="profile-name">{{ child.name }}</h1>
          <div class="profile-badges">
            <span class="profile-badge" v-if="child.gender">
              {{ child.gender === 'male' ? '男' : '女' }}
            </span>
            <span class="profile-badge" v-if="child.birthday">{{ calcAge(child.birthday) }}</span>
            <span class="profile-badge profile-badge--accent" v-if="child.class_name">
              {{ child.class_name }}
            </span>
          </div>
        </div>
      </div>
      <div class="profile-stats">
        <div class="profile-stat">
          <span class="profile-stat__value">{{ child.anecdote_count || 0 }}</span>
          <span class="profile-stat__label">观察记录</span>
        </div>
        <div class="profile-stat-divider"></div>
        <div class="profile-stat">
          <span class="profile-stat__value">{{ child.assessment_count || 0 }}</span>
          <span class="profile-stat__label">评估报告</span>
        </div>
      </div>
    </div>

    <!-- Domain Radar + Scores -->
    <div class="domain-section" v-if="child?.latest_scores">
      <div class="domain-radar-card">
        <h3 class="section-title">发展领域评估</h3>
        <DomainRadar :scores="child.latest_scores" :height="280" />
      </div>
      <div class="domain-scores-card">
        <h3 class="section-title">各领域得分</h3>
        <div class="domain-scores-list">
          <div v-for="domain in domains" :key="domain.key" class="domain-score-row">
            <div class="domain-score-row__header">
              <span class="domain-dot" :style="{ background: domain.color }"></span>
              <span class="domain-label">{{ domain.name }}</span>
              <span class="domain-value">{{ child.latest_scores[domain.key] || '-' }}</span>
            </div>
            <div class="domain-progress">
              <div
                class="domain-progress__fill"
                :style="{ width: ((child.latest_scores[domain.key] || 0) / 5 * 100) + '%', background: domain.color }"
              ></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Anecdote Timeline -->
    <div class="timeline-section">
      <div class="timeline-section__header">
        <h3 class="section-title">观察记录</h3>
        <router-link to="/anecdotes/new" class="timeline-new-btn">
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
            <path d="M7 1v12M1 7h12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          </svg>
          新建记录
        </router-link>
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
.profile-page {
  max-width: 960px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* ---- Profile Header ---- */
.profile-header {
  background: #fff;
  border-radius: var(--radius-xl);
  padding: 32px;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 24px;
}

.profile-header__main {
  display: flex;
  align-items: center;
  gap: 20px;
}

.profile-avatar {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 28px;
  font-weight: 700;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.profile-identity {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.profile-name {
  font-size: 24px;
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0;
  line-height: 1.3;
}

.profile-badges {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.profile-badge {
  display: inline-flex;
  align-items: center;
  padding: 3px 10px;
  border-radius: var(--radius-full);
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text-secondary);
  background: var(--color-bg-tertiary, #F5F5F4);
}

.profile-badge--accent {
  background: var(--color-accent-light);
  color: var(--color-accent);
  font-weight: 600;
}

.profile-stats {
  display: flex;
  align-items: center;
  gap: 24px;
}

.profile-stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}

.profile-stat__value {
  font-size: 28px;
  font-weight: 700;
  color: var(--color-text-primary);
  line-height: 1.2;
}

.profile-stat__label {
  font-size: 12px;
  color: var(--color-text-tertiary);
  font-weight: 500;
}

.profile-stat-divider {
  width: 1px;
  height: 36px;
  background: var(--color-border);
}

/* ---- Domain Section ---- */
.domain-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.domain-radar-card,
.domain-scores-card {
  background: #fff;
  border-radius: var(--radius-xl);
  padding: 24px;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border);
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 20px 0;
}

.domain-scores-list {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.domain-score-row__header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}

.domain-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}

.domain-label {
  font-size: 14px;
  color: var(--color-text-secondary);
  flex: 1;
  font-weight: 500;
}

.domain-value {
  font-size: 14px;
  font-weight: 700;
  color: var(--color-text-primary);
  min-width: 20px;
  text-align: right;
}

.domain-progress {
  height: 6px;
  background: var(--color-bg-tertiary, #F5F5F4);
  border-radius: 3px;
  overflow: hidden;
}

.domain-progress__fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

/* ---- Timeline Section ---- */
.timeline-section {
  background: #fff;
  border-radius: var(--radius-xl);
  padding: 24px;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border);
}

.timeline-section__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.timeline-section__header .section-title {
  margin-bottom: 0;
}

.timeline-new-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  border-radius: var(--radius-md);
  font-size: 13px;
  font-weight: 500;
  color: var(--color-accent);
  background: var(--color-accent-light);
  text-decoration: none;
  transition: background 0.15s ease;
}

.timeline-new-btn:hover {
  background: #E0E7FF;
}

/* ---- Responsive ---- */
@media (max-width: 768px) {
  .profile-header {
    flex-direction: column;
    align-items: flex-start;
    padding: 24px;
  }

  .profile-avatar {
    width: 60px;
    height: 60px;
    font-size: 24px;
  }

  .profile-name {
    font-size: 20px;
  }

  .profile-stat__value {
    font-size: 22px;
  }

  .domain-section {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .profile-page {
    gap: 16px;
  }

  .profile-header {
    padding: 20px;
  }

  .domain-radar-card,
  .domain-scores-card,
  .timeline-section {
    padding: 16px;
    border-radius: var(--radius-lg);
  }
}
</style>
