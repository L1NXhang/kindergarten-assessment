<template>
  <div class="child-selector">
    <select v-model="selectedId" class="form-select" @change="$emit('update:modelValue', selectedId)">
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
</style>
