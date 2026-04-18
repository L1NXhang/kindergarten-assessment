<template>
  <span class="name-tag" :style="{ background: bgColor, color: textColor }">
    {{ name }}
    <button v-if="removable" class="tag-close" @click.stop="$emit('remove', name)">
      <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
    </button>
  </span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  name: { type: String, required: true },
  color: { type: String, default: '' },
  removable: { type: Boolean, default: false }
})

defineEmits(['remove'])

const colors = [
  { bg: '#EFF6FF', text: '#2563EB' },
  { bg: '#ECFDF5', text: '#059669' },
  { bg: '#FFF7ED', text: '#D97706' },
  { bg: '#F5F3FF', text: '#7C3AED' },
  { bg: '#FDF2F8', text: '#DB2777' },
  { bg: '#ECFEFF', text: '#0891B2' },
  { bg: '#FEF2F2', text: '#DC2626' }
]

function hashString(str) {
  let hash = 0
  for (let i = 0; i < str.length; i++) {
    hash = str.charCodeAt(i) + ((hash << 5) - hash)
  }
  return Math.abs(hash)
}

const bgColor = computed(() => {
  if (props.color) return props.color + '20'
  return colors[hashString(props.name) % colors.length].bg
})

const textColor = computed(() => {
  if (props.color) return props.color
  return colors[hashString(props.name) % colors.length].text
})
</script>

<style scoped>
.name-tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px 12px;
  border-radius: var(--radius-full);
  font-size: var(--font-size-xs);
  font-weight: 500;
  white-space: nowrap;
  transition: all var(--transition-fast);
  line-height: 1.4;
}

.name-tag:hover {
  filter: brightness(0.96);
}

.tag-close {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 16px;
  height: 16px;
  border-radius: var(--radius-full);
  cursor: pointer;
  opacity: 0.5;
  transition: all var(--transition-fast);
  background: none;
  border: none;
  padding: 0;
  color: inherit;
  margin-left: 2px;
}

.tag-close:hover {
  opacity: 1;
  background: rgba(0, 0, 0, 0.08);
}
</style>
