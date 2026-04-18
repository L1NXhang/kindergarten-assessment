<template>
  <div class="assessment-card" @click="$emit('click')">
    <div class="card-top">
      <div class="card-info">
        <h4 class="card-title">{{ assessment.title || '评估报告' }}</h4>
        <p class="card-meta">
          <span>{{ assessment.class_name || '' }}</span>
          <span v-if="assessment.child_name" class="card-meta-sep">-</span>
          <span v-if="assessment.child_name">{{ assessment.child_name }}</span>
        </p>
      </div>
      <span class="status-pill" :style="{ background: statusColor + '14', color: statusColor }">
        {{ statusLabel }}
      </span>
    </div>

    <div class="card-body" v-if="assessment.scores">
      <div class="domain-scores">
        <div
          v-for="domain in domains"
          :key="domain.key"
          class="domain-item"
        >
          <span class="domain-dot" :style="{ background: domain.color }"></span>
          <span class="domain-label">{{ domain.name }}</span>
          <span class="domain-value">{{ assessment.scores[domain.key] || '-' }}</span>
        </div>
      </div>
    </div>

    <div class="card-footer">
      <span class="card-date">{{ formatDate(assessment.created_at) }}</span>
      <svg class="card-arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { ASSESSMENT_STATUS, DOMAINS } from '../../utils/constants.js'
import { formatDate } from '../../utils/format.js'

const props = defineProps({
  assessment: { type: Object, required: true }
})

defineEmits(['click'])

const domains = DOMAINS

const statusInfo = computed(() => {
  return ASSESSMENT_STATUS[props.assessment.status] || ASSESSMENT_STATUS.pending
})

const statusLabel = computed(() => statusInfo.value.label)
const statusColor = computed(() => statusInfo.value.color)
</script>

<style scoped>
.assessment-card {
  background: #fff;
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--radius-xl);
  padding: 20px 24px;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: var(--shadow-sm);
}

.assessment-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
  border-color: var(--color-border);
}

/* Card Top */
.card-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 16px;
}

.card-info {
  flex: 1;
  min-width: 0;
}

.card-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 4px 0;
  letter-spacing: -0.01em;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.card-meta {
  font-size: 13px;
  color: var(--color-text-tertiary);
  margin: 0;
  display: flex;
  align-items: center;
}

.card-meta-sep {
  margin: 0 4px;
}

.status-pill {
  display: inline-flex;
  align-items: center;
  padding: 3px 12px;
  border-radius: var(--radius-full);
  font-size: 12px;
  font-weight: 500;
  white-space: nowrap;
  flex-shrink: 0;
}

/* Card Body - Domain Scores */
.card-body {
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--color-border-subtle);
}

.domain-scores {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.domain-item {
  display: flex;
  align-items: center;
  gap: 5px;
}

.domain-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  flex-shrink: 0;
}

.domain-label {
  font-size: 12px;
  color: var(--color-text-tertiary);
}

.domain-value {
  font-size: 12px;
  font-weight: 600;
  color: var(--color-text-primary);
}

/* Card Footer */
.card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.card-date {
  font-size: 12px;
  color: var(--color-text-tertiary);
}

.card-arrow {
  color: var(--color-text-tertiary);
  opacity: 0;
  transform: translateX(-4px);
  transition: all 0.2s ease;
}

.assessment-card:hover .card-arrow {
  opacity: 1;
  transform: translateX(0);
}

/* Responsive */
@media (max-width: 480px) {
  .assessment-card {
    padding: 16px 18px;
  }

  .domain-scores {
    gap: 10px;
  }
}
</style>
