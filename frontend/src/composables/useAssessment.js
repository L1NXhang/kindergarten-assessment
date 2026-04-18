import { ref, computed } from 'vue'
import { useAssessmentStore } from '../stores/assessments.js'

export function useAssessment() {
  const store = useAssessmentStore()
  const selectedClassId = ref('')
  const selectedChildId = ref('')
  const assessmentType = ref('personal')

  const canGenerate = computed(() => {
    return selectedClassId.value || selectedChildId.value
  })

  async function createAndGenerate() {
    const data = {
      class_id: selectedClassId.value || undefined,
      child_id: selectedChildId.value || undefined,
      type: assessmentType.value
    }
    const assessment = await store.addAssessment(data)
    return await store.generateAssessmentReport(assessment.id)
  }

  async function refreshStatus(id) {
    return await store.fetchAssessmentById(id)
  }

  return {
    selectedClassId,
    selectedChildId,
    assessmentType,
    canGenerate,
    createAndGenerate,
    refreshStatus
  }
}
