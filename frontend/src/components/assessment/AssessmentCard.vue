<template>
  <div class="assessment-card card" @click="$emit('click')">
    <div class="assessment-card-header">
      <div class="assessment-card-info">
        <h4 class="assessment-card-title">{{ assessment.title || '评估报告' }}</h4>
        <p class="assessment-card-meta">
          <span>{{ assessment.class_name || '' }}</span>
          <span v-if="assessment.child_name"> - {{ assessment.child_name }}</span>
        </p>
      </div>
      <span class="badge" :style="{ background: statusColor + '15', color: statusColor }">
        {{ statusLabel }}
      </span>
    </div>
    <div class="assessment-card-body">
      <div class="assessment-card-stats" v-if="assessment.scores">
        <div
          v-for="domain in domains"
          :key="domain.key"
          class="domain-stat"
        >
          <span class="domain-dot" :style="{ background: domain.color }"></span>
          <span class="domain-name">{{ domain.name }}</span>
          <span class="domain-score">{{ assessment.scores[domain.key] || '-' }}</span>
        </div>
      </div>
      <div class="assessment-card-time">
        {{ formatDate(assessment.created_at) }}
      </div>
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
  cursor: pointer;
  transition: all 0.15s ease;
}

.assessment-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
}

.assessment-card-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 12px;
}

.assessment-card-title {
  font-size: var(--font-size-base);
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: 2px;
}

.assessment-card-meta {
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
}

.assessment-card-body {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
}

.assessment-card-stats {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.domain-stat {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: var(--font-size-xs);
}

.domain-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
}

.domain-name {
  color: var(--color-text-secondary);
}

.domain-score {
  font-weight: 600;
  color: var(--color-text-primary);
}

.assessment-card-time {
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
}
</style>
