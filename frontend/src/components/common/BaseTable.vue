<template>
  <div class="table-wrapper">
    <table class="data-table">
      <thead>
        <tr>
          <th v-for="col in columns" :key="col.key" :style="col.width ? { width: col.width } : {}">
            {{ col.label }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, index) in data" :key="row.id || index" class="table-row">
          <td v-for="col in columns" :key="col.key">
            <slot :name="`cell-${col.key}`" :row="row" :value="row[col.key]">
              {{ row[col.key] }}
            </slot>
          </td>
        </tr>
        <tr v-if="!data || data.length === 0">
          <td :colspan="columns.length" class="table-empty">
            <slot name="empty">
              <span class="table-empty-text">暂无数据</span>
            </slot>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
defineProps({
  columns: {
    type: Array,
    required: true
  },
  data: {
    type: Array,
    default: () => []
  }
})
</script>

<style scoped>
.table-wrapper {
  overflow-x: auto;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: #fff;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

.data-table thead tr {
  background: #FAF9F7;
}

.data-table th {
  padding: 10px 16px;
  text-align: left;
  font-size: 11px;
  font-weight: 600;
  color: var(--color-text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  white-space: nowrap;
  border-bottom: 1px solid var(--color-border);
}

.data-table td {
  padding: 10px 16px;
  color: var(--color-text-primary);
  border-bottom: 1px solid var(--color-border-subtle);
  white-space: nowrap;
}

.table-row:last-child td {
  border-bottom: none;
}

.table-row:nth-child(even) {
  background: #FDFCFA;
}

.table-row:hover {
  background: #FEF9F3;
}

.table-empty {
  text-align: center;
  padding: 40px 16px !important;
}

.table-empty-text {
  font-size: 13px;
  color: var(--color-text-tertiary);
}

@media (max-width: 768px) {
  .table-wrapper {
    border-radius: var(--radius-md);
  }

  .data-table th,
  .data-table td {
    padding: 10px 12px;
  }
}
</style>
