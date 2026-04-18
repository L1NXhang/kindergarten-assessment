<template>
  <div class="anecdote-card" @click="$emit('click')">
    <div class="anecdote-card-header">
      <div class="anecdote-card-meta">
        <span class="anecdote-card-time">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
          {{ time }}
        </span>
        <span class="anecdote-card-location" v-if="anecdote.location">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
          {{ anecdote.location }}
        </span>
        <span class="anecdote-card-activity" v-if="anecdote.activity_type">
          {{ anecdote.activity_type }}
        </span>
      </div>
      <div class="anecdote-card-actions" v-if="showActions">
        <slot name="actions"></slot>
      </div>
    </div>
    <p class="anecdote-card-content">{{ displayContent }}</p>
    <div class="anecdote-card-footer">
      <div class="anecdote-card-names" v-if="anecdote.children_names?.length">
        <NameTag
          v-for="name in anecdote.children_names"
          :key="name"
          :name="name"
        />
      </div>
      <span class="anecdote-card-teacher" v-if="anecdote.teacher_name">
        {{ anecdote.teacher_name }}
      </span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import NameTag from './NameTag.vue'
import { formatDate, truncateText } from '../../utils/format.js'

const props = defineProps({
  anecdote: { type: Object, required: true },
  showActions: { type: Boolean, default: false },
  maxContentLength: { type: Number, default: 120 }
})

defineEmits(['click'])

const time = computed(() => formatDate(props.anecdote.observation_time || props.anecdote.created_at))
const displayContent = computed(() => truncateText(props.anecdote.content, props.maxContentLength))
</script>

<style scoped>
.anecdote-card {
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 16px 20px;
  cursor: pointer;
  transition: all var(--transition-normal);
  box-shadow: var(--shadow-sm);
}

.anecdote-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
  border-color: transparent;
}

.anecdote-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.anecdote-card-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.anecdote-card-time {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
}

.anecdote-card-location {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
  padding: 2px 10px;
  background: var(--color-bg-primary);
  border-radius: var(--radius-full);
  border: 1px solid var(--color-border);
}

.anecdote-card-activity {
  font-size: var(--font-size-xs);
  color: var(--color-accent);
  padding: 2px 10px;
  background: var(--color-accent-light);
  border-radius: var(--radius-full);
  font-weight: 500;
}

.anecdote-card-actions {
  display: flex;
  gap: 4px;
  opacity: 0;
  transition: opacity var(--transition-fast);
}

.anecdote-card:hover .anecdote-card-actions {
  opacity: 1;
}

.anecdote-card-content {
  font-size: var(--font-size-sm);
  color: var(--color-text-primary);
  line-height: 1.75;
  margin-bottom: 14px;
}

.anecdote-card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.anecdote-card-names {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.anecdote-card-teacher {
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
  white-space: nowrap;
}

@media (max-width: 640px) {
  .anecdote-card {
    padding: 14px 16px;
  }

  .anecdote-card-meta {
    gap: 6px;
  }

  .anecdote-card-actions {
    opacity: 1;
  }
}
</style>
