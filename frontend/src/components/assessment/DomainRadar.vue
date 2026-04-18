<template>
  <div class="domain-radar">
    <canvas ref="canvasRef"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import { Chart, registerables } from 'chart.js'

Chart.register(...registerables)

const props = defineProps({
  scores: {
    type: Object,
    default: () => ({})
  },
  height: {
    type: Number,
    default: 300
  }
})

const canvasRef = ref(null)
let chartInstance = null

const labels = ['健康', '语言', '社会', '科学', '艺术']
const colors = ['#10B981', '#6366F1', '#F59E0B', '#8B5CF6', '#EC4899']

function createChart() {
  if (!canvasRef.value) return

  if (chartInstance) {
    chartInstance.destroy()
  }

  const ctx = canvasRef.value.getContext('2d')
  const data = labels.map((_, i) => {
    const key = ['health', 'language', 'social', 'science', 'art'][i]
    return props.scores[key] ?? 0
  })

  chartInstance = new Chart(ctx, {
    type: 'radar',
    data: {
      labels,
      datasets: [{
        label: '发展评估',
        data,
        backgroundColor: 'rgba(79, 70, 229, 0.08)',
        borderColor: '#4F46E5',
        borderWidth: 2,
        pointBackgroundColor: colors,
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointRadius: 5,
        pointHoverRadius: 7
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        }
      },
      scales: {
        r: {
          beginAtZero: true,
          max: 5,
          ticks: {
            stepSize: 1,
            font: { size: 11 },
            color: '#A8A29E',
            backdropColor: 'transparent'
          },
          pointLabels: {
            font: { size: 13, weight: '500' },
            color: '#57534E'
          },
          grid: {
            color: '#E8E5E0',
            lineWidth: 1
          },
          angleLines: {
            color: '#E8E5E0',
            lineWidth: 1
          }
        }
      }
    }
  })
}

onMounted(() => {
  nextTick(createChart)
})

watch(() => props.scores, () => {
  nextTick(createChart)
}, { deep: true })
</script>

<style scoped>
.domain-radar {
  width: 100%;
  height: v-bind(height + 'px');
  position: relative;
  max-width: 480px;
  margin: 0 auto;
}
</style>
