export const LOCATIONS = ['户外操场', '建构区', '阅读区', '美工区', '角色区', '科学区', '生活活动', '集体教学', '午睡', '其他']

export const ACTIVITY_TYPES = ['自由游戏', '集体教学', '区域活动', '生活活动', '户外活动']

export const AGE_GROUPS = ['3-4岁', '4-5岁', '5-6岁']

export const DOMAINS = [
  { key: 'health', name: '健康', color: '#10B981' },
  { key: 'language', name: '语言', color: '#3B82F6' },
  { key: 'social', name: '社会', color: '#F59E0B' },
  { key: 'science', name: '科学', color: '#8B5CF6' },
  { key: 'art', name: '艺术', color: '#EC4899' }
]

export const ASSESSMENT_STATUS = {
  pending: { label: '待生成', color: '#9B9B9B' },
  generating: { label: '生成中', color: '#2563EB' },
  completed: { label: '已完成', color: '#16A34A' },
  failed: { label: '生成失败', color: '#DC2626' }
}

export const GENDER_OPTIONS = [
  { value: 'male', label: '男' },
  { value: 'female', label: '女' }
]

export const LOCATION_ICONS = {
  '户外操场': '🌳',
  '建构区': '🧱',
  '阅读区': '📖',
  '美工区': '🎨',
  '角色区': '🎭',
  '科学区': '🔬',
  '生活活动': '🍽️',
  '集体教学': '📚',
  '午睡': '😴',
  '其他': '📌'
}
