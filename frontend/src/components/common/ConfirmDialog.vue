<template>
  <BaseModal v-model="visible" :title="title" size="sm">
    <div class="confirm-content">
      <div class="confirm-icon" :class="`confirm-icon-${type}`">
        <svg v-if="type === 'danger'" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
        <svg v-else width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
      </div>
      <p class="confirm-message">{{ message }}</p>
    </div>
    <template #footer>
      <button class="confirm-btn confirm-btn--cancel" @click="cancel">取消</button>
      <button class="confirm-btn" :class="type === 'danger' ? 'confirm-btn--danger' : 'confirm-btn--primary'" @click="confirm">
        {{ confirmText }}
      </button>
    </template>
  </BaseModal>
</template>

<script setup>
import { ref, watch } from 'vue'
import BaseModal from './BaseModal.vue'

const props = defineProps({
  modelValue: Boolean,
  title: { type: String, default: '确认操作' },
  message: { type: String, default: '确定要执行此操作吗？' },
  confirmText: { type: String, default: '确定' },
  type: { type: String, default: 'warning' }
})

const emit = defineEmits(['update:modelValue', 'confirm', 'cancel'])

const visible = ref(false)

watch(() => props.modelValue, (val) => {
  visible.value = val
})

watch(visible, (val) => {
  emit('update:modelValue', val)
})

function confirm() {
  visible.value = false
  emit('confirm')
}

function cancel() {
  visible.value = false
  emit('cancel')
}
</script>

<style scoped>
.confirm-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 12px 0;
}

.confirm-icon {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
  flex-shrink: 0;
}

.confirm-icon-danger {
  background: #FEF2F2;
  color: #DC2626;
}

.confirm-icon-warning {
  background: #FFFBEB;
  color: #D97706;
}

.confirm-message {
  font-size: 14px;
  color: var(--color-text-secondary);
  line-height: 1.6;
  margin: 0;
}

.confirm-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 8px 20px;
  font-size: 13px;
  font-weight: 500;
  border-radius: var(--radius-md);
  border: 1px solid transparent;
  cursor: pointer;
  transition: all var(--transition-fast);
  line-height: 1.4;
}

.confirm-btn--cancel {
  background: #fff;
  border-color: var(--color-border);
  color: var(--color-text-secondary);
}

.confirm-btn--cancel:hover {
  background: var(--color-border-subtle);
  color: var(--color-text-primary);
}

.confirm-btn--primary {
  background: var(--color-accent);
  color: #fff;
  border-color: var(--color-accent);
}

.confirm-btn--primary:hover {
  background: #4338CA;
  border-color: #4338CA;
}

.confirm-btn--danger {
  background: #DC2626;
  color: #fff;
  border-color: #DC2626;
}

.confirm-btn--danger:hover {
  background: #B91C1C;
  border-color: #B91C1C;
}
</style>
