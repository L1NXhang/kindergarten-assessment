<template>
  <div class="anecdote-form">
    <div class="form-group">
      <label class="form-label">班级</label>
      <div class="form-input-wrapper">
        <select v-model="form.class_id" class="form-select">
          <option value="">请选择班级</option>
          <option v-for="cls in classes" :key="cls.id" :value="cls.id">
            {{ cls.name }}
          </option>
        </select>
      </div>
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
      <div class="form-input-wrapper">
        <input
          type="datetime-local"
          v-model="form.observation_time"
          class="form-input"
        />
      </div>
    </div>

    <div class="form-group">
      <label class="form-label">活动类型</label>
      <div class="form-input-wrapper">
        <select v-model="form.activity_type" class="form-select">
          <option value="">请选择</option>
          <option v-for="type in activityTypes" :key="type" :value="type">
            {{ type }}
          </option>
        </select>
      </div>
    </div>

    <div class="form-group">
      <label class="form-label">
        观察内容
        <span class="form-label-hint">至少20字</span>
      </label>
      <textarea
        v-model="form.content"
        class="form-textarea"
        placeholder="请详细描述观察到的幼儿行为、语言、互动等..."
        rows="8"
        @input="onContentInput"
      ></textarea>
      <div class="form-hint-row">
        <span class="form-hint">{{ form.content?.length || 0 }} 字</span>
      </div>
    </div>

    <div class="form-group">
      <label class="form-label">关联幼儿</label>
      <div class="name-section">
        <div class="name-tags" v-if="form.children_names.length">
          <NameTag
            v-for="name in form.children_names"
            :key="name"
            :name="name"
            :removable="true"
            @remove="removeName"
          />
        </div>
        <div v-if="isRecognizing" class="recognizing-hint">
          <span class="loading-spinner" style="width:12px;height:12px;border-width:1.5px;"></span>
          正在识别姓名...
        </div>
        <div v-if="recognizedNames.length" class="recognized-names">
          <span class="recognized-label">识别到</span>
          <NameTag
            v-for="name in recognizedNames"
            :key="name"
            :name="name"
            @click="addName(name)"
            style="cursor:pointer;"
          />
        </div>
        <div class="add-name-row">
          <div class="add-name-input-wrapper">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="8.5" cy="7" r="4"/><line x1="20" y1="8" x2="20" y2="14"/><line x1="23" y1="11" x2="17" y2="11"/></svg>
            <input
              v-model="newName"
              class="add-name-input"
              placeholder="手动添加幼儿姓名"
              @keyup.enter="addNameFromInput"
            />
          </div>
          <button class="add-name-btn" @click="addNameFromInput">添加</button>
        </div>
      </div>
    </div>

    <div class="form-group">
      <label class="form-label">教师</label>
      <div class="form-input-wrapper">
        <input
          v-model="form.teacher_name"
          class="form-input"
          placeholder="教师姓名"
        />
      </div>
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
.anecdote-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* Form Groups */
.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  font-size: var(--font-size-sm);
  font-weight: 600;
  color: var(--color-text-primary);
}

.form-label-hint {
  font-weight: 400;
  color: var(--color-text-tertiary);
  margin-left: 4px;
}

/* Input Wrapper */
.form-input-wrapper {
  position: relative;
}

.form-input,
.form-select {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: var(--color-bg-secondary);
  font-size: var(--font-size-sm);
  color: var(--color-text-primary);
  outline: none;
  transition: all var(--transition-fast);
  box-sizing: border-box;
}

.form-input:focus,
.form-select:focus {
  border-color: var(--color-accent);
  box-shadow: 0 0 0 3px var(--color-accent-light);
}

.form-input::placeholder {
  color: var(--color-text-tertiary);
}

.form-select {
  appearance: none;
  -webkit-appearance: none;
  cursor: pointer;
  background-image: url("data:image/svg+xml,%3Csvg width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%23A8A29E' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 14px center;
  padding-right: 36px;
}

/* Location Tags */
.location-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.location-tag {
  display: inline-flex;
  align-items: center;
  padding: 6px 16px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-full);
  background: var(--color-bg-secondary);
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
  white-space: nowrap;
}

.location-tag:hover {
  border-color: var(--color-accent);
  color: var(--color-accent);
}

.location-tag.active {
  background: var(--color-accent-light);
  border-color: var(--color-accent);
  color: var(--color-accent);
  font-weight: 500;
}

/* Textarea */
.form-textarea {
  width: 100%;
  padding: 14px 16px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: var(--color-bg-secondary);
  font-size: var(--font-size-sm);
  color: var(--color-text-primary);
  line-height: 1.8;
  outline: none;
  transition: all var(--transition-fast);
  resize: vertical;
  min-height: 180px;
  box-sizing: border-box;
  font-family: inherit;
}

.form-textarea:focus {
  border-color: var(--color-accent);
  box-shadow: 0 0 0 3px var(--color-accent-light);
}

.form-textarea::placeholder {
  color: var(--color-text-tertiary);
}

.form-hint-row {
  display: flex;
  justify-content: flex-end;
}

.form-hint {
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
}

/* Name Section */
.name-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.name-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.recognizing-hint {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
}

.recognized-names {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 6px;
}

.recognized-label {
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
}

/* Add Name Row */
.add-name-row {
  display: flex;
  gap: 8px;
  align-items: center;
}

.add-name-input-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
  padding: 8px 14px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: var(--color-bg-secondary);
  transition: all var(--transition-fast);
  color: var(--color-text-tertiary);
}

.add-name-input-wrapper:focus-within {
  border-color: var(--color-accent);
  box-shadow: 0 0 0 3px var(--color-accent-light);
}

.add-name-input {
  flex: 1;
  border: none;
  background: transparent;
  font-size: var(--font-size-sm);
  color: var(--color-text-primary);
  outline: none;
  padding: 0;
}

.add-name-input::placeholder {
  color: var(--color-text-tertiary);
}

.add-name-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 8px 18px;
  border: 1px solid var(--color-accent);
  border-radius: var(--radius-lg);
  background: var(--color-accent);
  color: #fff;
  font-size: var(--font-size-sm);
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-fast);
  white-space: nowrap;
}

.add-name-btn:hover {
  background: #4338CA;
  border-color: #4338CA;
}

/* Responsive */
@media (max-width: 640px) {
  .anecdote-form {
    gap: 20px;
  }

  .location-tags {
    gap: 6px;
  }

  .location-tag {
    padding: 5px 12px;
    font-size: var(--font-size-xs);
  }

  .form-textarea {
    min-height: 140px;
    padding: 12px 14px;
  }
}
</style>
