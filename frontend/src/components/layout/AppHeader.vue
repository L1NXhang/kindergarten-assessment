<template>
  <header class="app-header">
    <div class="header-left">
      <button
        v-if="showMenuButton"
        class="menu-button"
        @click="$emit('toggle-sidebar')"
        aria-label="Toggle sidebar"
      >
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="3" y1="6" x2="21" y2="6"/>
          <line x1="3" y1="12" x2="21" y2="12"/>
          <line x1="3" y1="18" x2="21" y2="18"/>
        </svg>
      </button>
      <h2 class="header-title">{{ pageTitle }}</h2>
    </div>
    <div class="header-right">
      <router-link to="/anecdotes/new" class="btn-action">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <line x1="12" y1="5" x2="12" y2="19"/>
          <line x1="5" y1="12" x2="19" y2="12"/>
        </svg>
        <span class="btn-action-text">新建记录</span>
      </router-link>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

defineProps({
  showMenuButton: {
    type: Boolean,
    default: false
  }
})

defineEmits(['toggle-sidebar'])

const route = useRoute()

const pageTitle = computed(() => {
  return route.meta.title || '幼儿发展评估系统'
})
</script>

<style scoped>
.app-header {
  height: var(--header-height);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--color-border-subtle);
  position: sticky;
  top: 0;
  z-index: 50;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
}

.header-title {
  font-size: var(--font-size-xl);
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

/* Hamburger menu button */
.menu-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border: none;
  background: transparent;
  color: #374151;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: background-color 150ms ease;
  flex-shrink: 0;
}

.menu-button:hover {
  background: rgba(0, 0, 0, 0.05);
}

.menu-button:active {
  background: rgba(0, 0, 0, 0.08);
}

/* Quick action button */
.btn-action {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: #6366F1;
  color: #ffffff;
  border-radius: 9999px;
  font-size: var(--font-size-sm);
  font-weight: 500;
  text-decoration: none;
  transition: background-color 200ms ease, box-shadow 200ms ease;
  white-space: nowrap;
}

.btn-action:hover {
  background: #4F46E5;
  box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3);
}

.btn-action:active {
  background: #4338CA;
}

/* Responsive */
@media (max-width: 767px) {
  .app-header {
    padding: 0 16px;
  }

  .btn-action-text {
    display: none;
  }

  .btn-action {
    padding: 8px;
    border-radius: var(--radius-md);
  }
}
</style>
