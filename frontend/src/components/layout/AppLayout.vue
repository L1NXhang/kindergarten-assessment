<template>
  <div class="app-layout" :class="{ 'sidebar-open': sidebarOpen }">
    <!-- Mobile backdrop -->
    <Transition name="fade">
      <div
        v-if="isMobile && sidebarOpen"
        class="sidebar-backdrop"
        @click="sidebarOpen = false"
      ></div>
    </Transition>

    <AppSidebar :collapsed="isMobile ? !sidebarOpen : false" />

    <div class="app-main" :class="{ 'sidebar-visible': !isMobile }">
      <AppHeader
        @toggle-sidebar="sidebarOpen = !sidebarOpen"
        :show-menu-button="isMobile"
      />
      <main class="app-content">
        <router-view v-slot="{ Component }">
          <transition name="page" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, provide, onMounted, onUnmounted } from 'vue'
import AppSidebar from './AppSidebar.vue'
import AppHeader from './AppHeader.vue'

const MOBILE_BREAKPOINT = 1024

const isMobile = ref(false)
const sidebarOpen = ref(true)

function checkMobile() {
  const wasMobile = isMobile.value
  isMobile.value = !window.matchMedia(`(min-width: ${MOBILE_BREAKPOINT}px)`).matches

  // Auto-close sidebar when switching to mobile
  if (!wasMobile && isMobile.value) {
    sidebarOpen.value = false
  }
  // Auto-open sidebar when switching to desktop
  if (wasMobile && !isMobile.value) {
    sidebarOpen.value = true
  }
}

let mediaQuery = null

onMounted(() => {
  checkMobile()
  mediaQuery = window.matchMedia(`(min-width: ${MOBILE_BREAKPOINT}px)`)
  mediaQuery.addEventListener('change', checkMobile)
  window.addEventListener('resize', checkMobile)
})

onUnmounted(() => {
  if (mediaQuery) {
    mediaQuery.removeEventListener('change', checkMobile)
  }
  window.removeEventListener('resize', checkMobile)
})

function toggleSidebar() {
  sidebarOpen.value = !sidebarOpen.value
}

provide('toggleSidebar', toggleSidebar)
provide('isMobile', isMobile)
</script>

<style scoped>
.app-layout {
  display: flex;
  min-height: 100vh;
}

.app-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  margin-left: 0;
  transition: margin-left 300ms ease;
}

.app-main.sidebar-visible {
  margin-left: var(--sidebar-width);
}

.app-content {
  flex: 1;
  background: var(--color-bg-primary);
  overflow-y: auto;
  padding: 24px;
}

/* Sidebar backdrop for mobile */
.sidebar-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 90;
  backdrop-filter: blur(2px);
}

/* Backdrop fade transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 250ms ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Page transition */
.page-enter-active,
.page-leave-active {
  transition: opacity 200ms ease, transform 200ms ease;
}

.page-enter-from {
  opacity: 0;
  transform: translateY(6px);
}

.page-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}

/* Responsive adjustments */
@media (max-width: 767px) {
  .app-content {
    padding: 16px;
  }
}
</style>
