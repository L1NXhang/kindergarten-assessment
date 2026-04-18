import { ref } from 'vue'
import * as reportApi from '../api/reports.js'
import { useToast } from './useToast.js'

export function useExport() {
  const exporting = ref(false)
  const toast = useToast()

  async function exportReport(id, format = 'pdf', filename = 'report') {
    exporting.value = true
    try {
      const blob = await reportApi.exportReport(id, format)
      downloadBlob(blob, `${filename}.${format}`)
      toast.success('导出成功')
    } catch {
      toast.error('导出失败')
    } finally {
      exporting.value = false
    }
  }

  async function exportClassReport(classId, params, filename = 'class-report') {
    exporting.value = true
    try {
      const blob = await reportApi.exportClassReport(classId, params)
      downloadBlob(blob, `${filename}.pdf`)
      toast.success('导出成功')
    } catch {
      toast.error('导出失败')
    } finally {
      exporting.value = false
    }
  }

  async function exportChildReport(childId, params, filename = 'child-report') {
    exporting.value = true
    try {
      const blob = await reportApi.exportChildReport(childId, params)
      downloadBlob(blob, `${filename}.pdf`)
      toast.success('导出成功')
    } catch {
      toast.error('导出失败')
    } finally {
      exporting.value = false
    }
  }

  function downloadBlob(blob, filename) {
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = filename
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
  }

  return {
    exporting,
    exportReport,
    exportClassReport,
    exportChildReport
  }
}
