<template>
  <div class="anecdote-timeline">
    <div class="timeline" v-if="anecdotes.length > 0">
      <div
        v-for="anecdote in anecdotes"
        :key="anecdote.id"
        class="timeline-item"
      >
        <div class="timeline-dot"></div>
        <div class="timeline-content">
          <div class="timeline-header">
            <span class="timeline-time">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
              {{ formatDate(anecdote.observation_time || anecdote.created_at) }}
            </span>
            <span class="timeline-location" v-if="anecdote.location">
              <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
              {{ anecdote.location }}
            </span>
          </div>
          <p class="timeline-text">{{ anecdote.content }}</p>
          <div class="timeline-names" v-if="anecdote.children_names?.length">
            <NameTag
              v-for="name in anecdote.children_names"
              :key="name"
              :name="name"
            />
          </div>
        </div>
      </div>
    </div>
    <EmptyState v-else title="暂无观察记录" description="还没有该幼儿的观察记录" />
  </div>
</template>

<script setup>
import EmptyState from '../common/EmptyState.vue'
import NameTag from './NameTag.vue'
import { formatDate } from '../../utils/format.js'

defineProps({
  anecdotes: { type: Array, default: () => [] }
})
</script>

<style scoped>
.anecdote-timeline {
  padding: 4px 0;
}

.timeline {
  position: relative;
  padding-left: 28px;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 7px;
  top: 8px;
  bottom: 8px;
  width: 2px;
  background: var(--color-border);
  border-radius: 1px;
}

.timeline-item {
  position: relative;
  padding-bottom: 24px;
}

.timeline-item:last-child {
  padding-bottom: 0;
}

.timeline-dot {
  position: absolute;
  left: -28px;
  top: 6px;
  width: 12px;
  height: 12px;
  border-radius: var(--radius-full);
  background: var(--color-bg-secondary);
  border: 2px solid var(--color-accent);
  box-shadow: 0 0 0 3px var(--color-accent-light);
  z-index: 1;
}

.timeline-content {
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 14px 18px;
  transition: all var(--transition-normal);
}

.timeline-content:hover {
  box-shadow: var(--shadow-sm);
  border-color: transparent;
}

.timeline-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
  flex-wrap: wrap;
}

.timeline-time {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
}

.timeline-location {
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

.timeline-text {
  font-size: var(--font-size-sm);
  color: var(--color-text-primary);
  line-height: 1.75;
  margin-bottom: 10px;
}

.timeline-names {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

@media (max-width: 640px) {
  .timeline {
    padding-left: 24px;
  }

  .timeline::before {
    left: 5px;
  }

  .timeline-dot {
    left: -24px;
    width: 10px;
    height: 10px;
  }

  .timeline-content {
    padding: 12px 14px;
  }
}
</style>
