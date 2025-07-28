<template>
  <div>
    <canvas ref="canvas"></canvas>
  </div>
</template>

<script>
import {
  Chart,
  BarController,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from "chart.js";

Chart.register(
  BarController,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend
);

export default {
  name: "BarChart",
  props: {
    labels: Array,
    values: Array,
    label: String,
    colors: {
      type: Array,
      default: () => ["#4adbca"],
    },
  },
  mounted() {
    new Chart(this.$refs.canvas, {
      type: "bar",
      data: {
        labels: this.labels,
        datasets: [
          {
            label: this.label,
            data: this.values,
            backgroundColor:
              this.colors.length === this.values.length
                ? this.colors
                : Array(this.values.length).fill(this.colors[0]),
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: false },
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              stepSize: 1,
            },
          },
        },
      },
    });
  },
};
</script>

<!-- 
pastelColors: ['#a3cef1', '#fcd5ce', '#cdb4db', '#b5ead7', '#f9dc5c']
vividColors: ['#ff595e', '#1982c4', '#6a4c93', '#8ac926', '#ffca3a']
coolColors: ['#4adbca', '#70d6ff', '#96f7d2', '#caffbf', '#a0c4ff'] -->
