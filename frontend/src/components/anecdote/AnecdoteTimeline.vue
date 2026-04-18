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
            <span class="timeline-time">{{ formatDate(anecdote.observation_time || anecdote.created_at) }}</span>
            <span class="timeline-location">{{ anecdote.location }}</span>
          </div>
          <p class="timeline-text">{{ anecdote.content }}</p>
          <div class="tag-group mt-sm" v-if="anecdote.children_names?.length">
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
.timeline-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 6px;
}

.timeline-time {
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
}

.timeline-location {
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
  padding: 1px 8px;
  background: var(--color-bg-tertiary);
  border-radius: 8px;
}

.timeline-text {
  font-size: var(--font-size-sm);
  color: var(--color-text-primary);
  line-height: 1.7;
}
</style>
