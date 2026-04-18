<template>
  <div class="anecdote-card card" @click="$emit('click')">
    <div class="anecdote-card-header">
      <div class="anecdote-card-meta">
        <span class="anecdote-card-time">{{ time }}</span>
        <span class="anecdote-card-location">
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
      <div class="tag-group" v-if="anecdote.children_names?.length">
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
  cursor: pointer;
  transition: all 0.15s ease;
}

.anecdote-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
}

.anecdote-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}

.anecdote-card-meta {
  display: flex;
  align-items: center;
  gap: 12px;
}

.anecdote-card-time {
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
}

.anecdote-card-location {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
}

.anecdote-card-activity {
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
  padding: 1px 8px;
  background: var(--color-bg-tertiary);
  border-radius: 8px;
}

.anecdote-card-actions {
  display: flex;
  gap: 4px;
}

.anecdote-card-content {
  font-size: var(--font-size-sm);
  color: var(--color-text-primary);
  line-height: 1.7;
  margin-bottom: 12px;
}

.anecdote-card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.anecdote-card-teacher {
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
}
</style>
