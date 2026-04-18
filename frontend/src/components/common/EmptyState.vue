<template>
  <div class="empty-state">
    <div class="empty-state-icon">
      <slot name="icon">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/></svg>
      </slot>
    </div>
    <h3 class="empty-state-title">{{ title }}</h3>
    <p class="empty-state-desc">{{ description }}</p>
    <slot name="action"></slot>
  </div>
</template>

<script setup>
defineProps({
  title: { type: String, default: '暂无数据' },
  description: { type: String, default: '' }
})
</script>

<style scoped>
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
}

.empty-state-icon {
  color: var(--color-text-tertiary);
  margin-bottom: 16px;
  opacity: 0.4;
}

.empty-state-title {
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--color-text-secondary);
  margin-bottom: 8px;
}

.empty-state-desc {
  font-size: var(--font-size-sm);
  color: var(--color-text-tertiary);
  max-width: 400px;
  margin-bottom: 20px;
}
</style>
