<template>
  <div class="child-card" @click="$emit('click')">
    <div class="child-card__avatar" :style="{ background: avatarColor }">
      {{ avatarText }}
    </div>
    <div class="child-card__body">
      <span class="child-card__name">{{ child.name }}</span>
      <span class="child-card__meta">
        {{ genderLabel }}<template v-if="child.age"> · {{ child.age }}</template>
      </span>
    </div>
    <div class="child-card__count" v-if="child.anecdote_count !== undefined">
      {{ child.anecdote_count }} 条记录
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  child: { type: Object, required: true }
})

defineEmits(['click'])

const avatarText = computed(() => {
  return (props.child.name || '?').slice(-1)
})

const avatarColor = computed(() => {
  const colors = ['#3B82F6', '#10B981', '#F59E0B', '#8B5CF6', '#EC4899', '#06B6D4']
  const index = (props.child.name || '').charCodeAt(0) % colors.length
  return colors[index]
})

const genderLabel = computed(() => {
  if (props.child.gender === 'male') return '男'
  if (props.child.gender === 'female') return '女'
  return ''
})
</script>

<style scoped>
.child-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: #fff;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  box-shadow: var(--shadow-sm);
}

.child-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.child-card__avatar {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  flex-shrink: 0;
}

.child-card__body {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.child-card__name {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-primary);
  line-height: 1.3;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.child-card__meta {
  font-size: 12px;
  color: var(--color-text-tertiary);
  line-height: 1.3;
}

.child-card__count {
  flex-shrink: 0;
  font-size: 12px;
  color: var(--color-text-tertiary);
  white-space: nowrap;
  padding: 3px 8px;
  background: var(--color-bg-tertiary, #F5F5F4);
  border-radius: var(--radius-full);
}
</style>
