<template>
  <div>
    <canvas ref="canvas"></canvas>
  </div>
</template>

<script>
import { Chart, PieController, ArcElement, Tooltip, Legend } from "chart.js";

Chart.register(PieController, ArcElement, Tooltip, Legend);

export default {
  name: "PieChart",
  props: {
    data: Object,
    colors: {
      type: Array,
      default: () => ["#4caf50", "#ff9800", "#f44336"], // Default: High, Moderate, Low
    },
  },
  mounted() {
    new Chart(this.$refs.canvas, {
      type: "pie",
      data: {
        labels: ["High", "Moderate", "Low"],
        datasets: [
          {
            data: [this.data.high, this.data.moderate, this.data.low],
            backgroundColor: this.colors,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: "bottom",
          },
        },
      },
    });
  },
};
</script>

<style scoped>
canvas {
  max-width: 400px;
}
</style>
