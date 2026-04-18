<template>
  <div class="trend-chart">
    <canvas ref="canvasRef"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import { Chart, registerables } from 'chart.js'

Chart.register(...registerables)

const props = defineProps({
  labels: { type: Array, default: () => [] },
  datasets: { type: Array, default: () => [] },
  height: { type: Number, default: 300 }
})

const canvasRef = ref(null)
let chartInstance = null

function createChart() {
  if (!canvasRef.value) return

  if (chartInstance) {
    chartInstance.destroy()
  }

  const ctx = canvasRef.value.getContext('2d')

  chartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: props.labels,
      datasets: props.datasets.map(ds => ({
        ...ds,
        tension: 0.3,
        borderWidth: 2,
        pointRadius: 4,
        pointHoverRadius: 6,
        fill: false
      }))
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: props.datasets.length > 1,
          position: 'top',
          labels: {
            usePointStyle: true,
            padding: 16,
            font: { size: 12 }
          }
        }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { font: { size: 11 }, color: '#9B9B9B' }
        },
        y: {
          beginAtZero: true,
          max: 5,
          ticks: {
            stepSize: 1,
            font: { size: 11 },
            color: '#9B9B9B'
          },
          grid: { color: '#F0F0F0' }
        }
      },
      interaction: {
        intersect: false,
        mode: 'index'
      }
    }
  })
}

onMounted(() => {
  nextTick(createChart)
})

watch([() => props.labels, () => props.datasets], () => {
  nextTick(createChart)
}, { deep: true })
</script>

<style scoped>
.trend-chart {
  width: 100%;
  height: v-bind(height + 'px');
  position: relative;
}
</style>
