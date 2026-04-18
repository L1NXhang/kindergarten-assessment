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
        pointBackgroundColor: '#4F46E5',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        borderColor: '#4F46E5',
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
            pointStyle: 'circle',
            padding: 20,
            font: { size: 12, weight: '500' },
            color: '#57534E'
          }
        }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { font: { size: 12 }, color: '#A8A29E' },
          border: { display: false }
        },
        y: {
          beginAtZero: true,
          max: 5,
          ticks: {
            stepSize: 1,
            font: { size: 11 },
            color: '#A8A29E',
            padding: 8
          },
          grid: {
            color: '#F0EDE8',
            lineWidth: 1
          },
          border: { display: false }
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
