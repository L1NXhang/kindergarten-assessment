<template>
  <div class="child-card card" @click="$emit('click')">
    <div class="child-card-avatar" :style="{ background: avatarColor }">
      {{ avatarText }}
    </div>
    <div class="child-card-info">
      <h4 class="child-card-name">{{ child.name }}</h4>
      <p class="child-card-meta">
        <span>{{ genderLabel }}</span>
        <span v-if="child.age"> · {{ child.age }}</span>
      </p>
    </div>
    <div class="child-card-stats" v-if="child.anecdote_count !== undefined">
      <span class="text-xs text-tertiary">{{ child.anecdote_count }} 条记录</span>
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
  cursor: pointer;
  transition: all 0.15s ease;
  padding: 14px 16px;
}

.child-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
}

.child-card-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: var(--font-size-sm);
  font-weight: 600;
  flex-shrink: 0;
}

.child-card-info {
  flex: 1;
  min-width: 0;
}

.child-card-name {
  font-size: var(--font-size-sm);
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: 1px;
}

.child-card-meta {
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
}

.child-card-stats {
  flex-shrink: 0;
}
</style>
