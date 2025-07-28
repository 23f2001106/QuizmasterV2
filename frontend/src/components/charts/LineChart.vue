<template>
  <canvas ref="canvas"></canvas>
</template>

<script>
import {
  Chart,
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Tooltip,
  Legend,
} from "chart.js";

Chart.register(
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Tooltip,
  Legend
);

export default {
  name: "LineChart",
  props: {
    data: Array,
    color: {
      type: String,
      default: "#4adbca",
    },
  },
  mounted() {
    new Chart(this.$refs.canvas, {
      type: "line",
      data: {
        labels: this.data.map((p) => p.date),
        datasets: [
          {
            label: "Value",
            data: this.data.map((p) => p.value),
            borderColor: this.color,
            backgroundColor: this.color + "33",
            fill: false,
            tension: 0.3,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            display: false,
          },
        },
      },
    });
  },
};
</script>
