<template>
  <div class="anecdote-form">
    <div class="form-group">
      <label class="form-label">班级</label>
      <select v-model="form.class_id" class="form-select">
        <option value="">请选择班级</option>
        <option v-for="cls in classes" :key="cls.id" :value="cls.id">
          {{ cls.name }}
        </option>
      </select>
    </div>

    <div class="form-group">
      <label class="form-label">观察地点</label>
      <div class="location-tags">
        <button
          v-for="loc in locations"
          :key="loc"
          class="location-tag"
          :class="{ active: form.location === loc }"
          @click="form.location = loc"
        >
          {{ loc }}
        </button>
      </div>
    </div>

    <div class="form-group">
      <label class="form-label">观察时间</label>
      <input
        type="datetime-local"
        v-model="form.observation_time"
        class="form-input"
      />
    </div>

    <div class="form-group">
      <label class="form-label">活动类型</label>
      <select v-model="form.activity_type" class="form-select">
        <option value="">请选择</option>
        <option v-for="type in activityTypes" :key="type" :value="type">
          {{ type }}
        </option>
      </select>
    </div>

    <div class="form-group">
      <label class="form-label">观察内容 <span class="text-tertiary text-xs">（至少20字）</span></label>
      <textarea
        v-model="form.content"
        class="form-textarea"
        placeholder="请详细描述观察到的幼儿行为、语言、互动等..."
        rows="8"
        @input="onContentInput"
      ></textarea>
      <p class="form-hint">{{ form.content?.length || 0 }} 字</p>
    </div>

    <div class="form-group">
      <label class="form-label">关联幼儿</label>
      <div class="tag-group mb-sm" v-if="form.children_names.length">
        <NameTag
          v-for="name in form.children_names"
          :key="name"
          :name="name"
          :removable="true"
          @remove="removeName"
        />
      </div>
      <div v-if="isRecognizing" class="recognizing-hint text-xs text-tertiary">
        <span class="loading-spinner" style="width:12px;height:12px;border-width:1.5px;"></span>
        正在识别姓名...
      </div>
      <div v-if="recognizedNames.length" class="recognized-names">
        <span class="text-xs text-tertiary">识别到：</span>
        <NameTag
          v-for="name in recognizedNames"
          :key="name"
          :name="name"
          @click="addName(name)"
          style="cursor:pointer;"
        />
      </div>
      <div class="add-name-row mt-sm">
        <input
          v-model="newName"
          class="form-input"
          placeholder="手动添加幼儿姓名"
          style="flex:1"
          @keyup.enter="addNameFromInput"
        />
        <button class="btn btn-secondary btn-sm" @click="addNameFromInput">添加</button>
      </div>
    </div>

    <div class="form-group">
      <label class="form-label">教师</label>
      <input
        v-model="form.teacher_name"
        class="form-input"
        placeholder="教师姓名"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import NameTag from './NameTag.vue'
import { LOCATIONS, ACTIVITY_TYPES } from '../../utils/constants.js'

const props = defineProps({
  form: { type: Object, required: true },
  classes: { type: Array, default: () => [] },
  recognizedNames: { type: Array, default: () => [] },
  isRecognizing: { type: Boolean, default: false }
})

const emit = defineEmits(['content-change', 'add-name', 'remove-name'])

const locations = LOCATIONS
const activityTypes = ACTIVITY_TYPES
const newName = ref('')

function onContentInput() {
  emit('content-change', props.form.content)
}

function addName(name) {
  emit('add-name', name)
}

function removeName(name) {
  emit('remove-name', name)
}

function addNameFromInput() {
  if (newName.value.trim()) {
    addName(newName.value.trim())
    newName.value = ''
  }
}
</script>

<style scoped>
.recognizing-hint {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 8px;
}

.recognized-names {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 8px;
}

.add-name-row {
  display: flex;
  gap: 8px;
}
</style>
