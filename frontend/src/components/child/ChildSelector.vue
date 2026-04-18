<template>
  <div class="child-selector">
    <select v-model="selectedId" class="child-selector__input" @change="$emit('update:modelValue', selectedId)">
      <option value="">请选择幼儿</option>
      <optgroup v-for="group in groupedChildren" :key="group.label" :label="group.label">
        <option v-for="child in group.children" :key="child.id" :value="child.id">
          {{ child.name }}
        </option>
      </optgroup>
    </select>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  children: { type: Array, default: () => [] },
  modelValue: { type: [String, Number], default: '' }
})

const emit = defineEmits(['update:modelValue'])

const selectedId = ref(props.modelValue)

watch(() => props.modelValue, (val) => {
  selectedId.value = val
})

const groupedChildren = computed(() => {
  const groups = {}
  props.children.forEach(child => {
    const label = child.class_name || '未分组'
    if (!groups[label]) {
      groups[label] = { label, children: [] }
    }
    groups[label].children.push(child)
  })
  return Object.values(groups)
})
</script>

<style scoped>
.child-selector {
  width: 100%;
}

.child-selector__input {
  width: 100%;
  padding: 9px 12px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  font-size: 14px;
  color: var(--color-text-primary);
  background: #fff;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg width='10' height='6' viewBox='0 0 10 6' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M1 1l4 4 4-4' stroke='%23A8A29E' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  padding-right: 32px;
  cursor: pointer;
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
  box-sizing: border-box;
}

.child-selector__input:focus {
  outline: none;
  border-color: var(--color-accent);
  box-shadow: 0 0 0 3px var(--color-accent-light);
}

.child-selector__input optgroup {
  font-weight: 600;
  color: var(--color-text-secondary);
}

.child-selector__input option {
  font-weight: 400;
  padding: 4px 0;
}
</style>
