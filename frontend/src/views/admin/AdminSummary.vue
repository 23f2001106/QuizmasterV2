<template>
  <div class="summary-layout">
    <SideBar />

    <div class="main-content">
      <BaseLoader v-if="loading" />

      <div v-else>
        <header class="summary-header">
          <h2>Welcome, Admin</h2>
        </header>

        <!-- Charts Section -->
        <section class="charts">
          <div class="chart-row">
            <div class="chart-card">
              <h3>Average Score per Subject</h3>
              <BarChart
                v-if="charts.average_score_per_subject.length"
                :labels="charts.average_score_per_subject.map((s) => s.label)"
                :values="charts.average_score_per_subject.map((s) => s.value)"
                label="Average Score"
                :colors="pastelColors"
              />
              <p v-else>No data available.</p>
            </div>

            <div class="chart-card">
              <h3>Highest Score per Quiz</h3>
              <BarChart
                v-if="charts.highest_score_per_quiz.length"
                :labels="charts.highest_score_per_quiz.map((q) => q.label)"
                :values="charts.highest_score_per_quiz.map((q) => q.value)"
                label="Highest Score"
                :colors="vividColors"
              />
              <p v-else>No data available.</p>
            </div>
          </div>

          <div class="chart-row">
            <div class="chart-card">
              <h3>Attempts per Quiz</h3>
              <BarChart
                v-if="charts.attempts_per_quiz.length"
                :labels="charts.attempts_per_quiz.map((q) => q.label)"
                :values="charts.attempts_per_quiz.map((q) => q.value)"
                label="Attempts"
                :colors="barColors"
              />
              <p v-else>No data available.</p>
            </div>

            <div class="chart-card">
              <h3>Attempts per Subject</h3>
              <BarChart
                v-if="charts.attempts_per_subject.length"
                :labels="charts.attempts_per_subject.map((s) => s.label)"
                :values="charts.attempts_per_subject.map((s) => s.value)"
                label="Attempts"
                :colors="coolColors"
              />
              <p v-else>No data available.</p>
            </div>
          </div>

          <div class="chart-row">
            <div class="chart-card pie-chart-card">
              <h3>Score Distribution</h3>
              <PieChart
                v-if="hasScoreData"
                :data="charts.score_distribution"
                :colors="['#4caf50', '#ffc107', '#f44336']"
              />
              <p v-else>No score data.</p>
            </div>

            <div class="chart-card">
              <h3>Attempts in Last 7 Days</h3>
              <LineChart
                v-if="charts.attempts_per_day.length"
                :data="charts.attempts_per_day"
                :color="'#4a90e2'"
              />
              <p v-else>No attempt data.</p>
            </div>
          </div>
        </section>

        <!-- User Activity Section -->
        <section class="user-activity-section">
          <h3 class="section-heading">User Activity (Last 7 Days)</h3>
          <div class="chart-row">
            <div class="chart-card">
              <h3>New Users (Last 7 Days)</h3>
              <LineChart
                v-if="charts.user_activity.new_users_last_7_days.length"
                :data="charts.user_activity.new_users_last_7_days"
                :color="'#26c6da'"
              />
              <p v-else>No new users.</p>
            </div>

            <div class="chart-card">
              <h3>Logins (Last 7 Days)</h3>
              <LineChart
                v-if="charts.user_activity.logins_last_7_days.length"
                :data="charts.user_activity.logins_last_7_days"
                :color="'#7e57c2'"
              />
              <p v-else>No login data.</p>
            </div>
          </div>

          <div class="stat-card single-stat">
            <div class="card-body">
              <div class="card-title">Active Users</div>
              <div class="stat-value">
                {{ charts.user_activity.active_users_last_7_days }}
              </div>
            </div>
          </div>
        </section>

        <!-- Leaderboard -->
        <section class="leaderboard-card">
          <h3>Top Performers</h3>
          <table v-if="tables.leaderboard.length">
            <thead>
              <tr>
                <th>User</th>
                <th>Username</th>
                <th>Avg Score</th>
                <th>Quizzes Attempted</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(u, idx) in tables.leaderboard" :key="idx">
                <td>{{ u.user }}</td>
                <td>{{ u.username }}</td>
                <td>{{ u.average_score }}%</td>
                <td>{{ u.quizzes_attempted }}</td>
              </tr>
            </tbody>
          </table>
          <p v-else>No leaderboard data.</p>
        </section>
      </div>
    </div>
  </div>
  <AppFooter />
</template>

<script>
import axios from "axios";
import SideBar from "@/components/admin/SideBar.vue";
import AppFooter from "@/components/AppFooter.vue";
import BaseLoader from "@/components/BaseLoader.vue";
import LineChart from "@/components/charts/LineChart.vue";
import PieChart from "@/components/charts/PieChart.vue";
import BarChart from "@/components/charts/BarChart.vue";

export default {
  name: "AdminSummary",
  components: {
    SideBar,
    AppFooter,
    BaseLoader,
    LineChart,
    PieChart,
    BarChart,
  },
  data() {
    return {
      charts: {},
      tables: {},
      loading: true,
      pastelColors: ["#a3cef1", "#fcd5ce", "#cdb4db", "#b5ead7", "#f9dc5c"],
      vividColors: ["#ff595e", "#1982c4", "#6a4c93", "#8ac926", "#ffca3a"],
      coolColors: ["#4adbca", "#70d6ff", "#96f7d2", "#caffbf", "#a0c4ff"],
      barColors: [
        "#42a5f5",
        "#66bb6a",
        "#ffa726",
        "#ab47bc",
        "#26c6da",
        "#ef5350",
        "#7e57c2",
        "#26a69a",
        "#ff7043",
      ],
    };
  },
  mounted() {
    this.fetchSummary();
  },
  computed: {
    hasScoreData() {
      return Object.values(this.charts.score_distribution || {}).some(
        (v) => v > 0
      );
    },
  },
  methods: {
    async fetchSummary() {
      try {
        const res = await axios.get("/admin/summary");
        this.charts = res.data.charts;
        this.tables = res.data.tables;
      } catch (err) {
        console.error("Failed to load admin summary:", err);
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.summary-layout {
  display: flex;
  min-height: 100vh;
  background-color: #f9f9f9;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 1.5rem;
}

.summary-header {
  margin-bottom: 2rem;
  font-size: 1.5rem;
  font-weight: 600;
}

.chart-row {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 20px;
}

.chart-card,
.stat-card,
.leaderboard-card {
  background: #fff;
  border-radius: 8px;
  padding: 16px;
  flex: 1;
  min-width: 300px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
}

.chart-card:hover,
.stat-card:hover,
.leaderboard-card:hover {
  transform: scale(1.02);
}

.pie-chart-card {
  max-width: 400px;
  aspect-ratio: 1 / 1;
  margin: 0 auto;
}

.stat-card.single-stat {
  max-width: 300px;
  margin-top: 10px;
}

.stat-value {
  font-size: 2rem;
  font-weight: bold;
  color: #4a90e2;
}

.user-activity-section {
  margin-top: 40px;
  margin-bottom: 30px;
}

.user-activity-section h3 {
  margin-bottom: 10px;
  font-size: 1.4rem;
  font-weight: 600;
}

.stat-card .card-title {
  font-weight: 600;
  margin-bottom: 4px;
}

.section-heading {
  padding-bottom: 20px;
}

table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  margin-top: 10px;
  background-color: #ffffff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

th,
td {
  padding: 12px 14px;
  text-align: left;
  border-bottom: 1px solid #e0e6ed;
  font-size: 14px;
  color: #333;
}

th {
  font-weight: 600;
  color: #2c3e50;
  background-color: #b0e0fe;
}

tbody tr:nth-child(even) {
  background-color: #fafbfc;
}

tbody tr:hover {
  background-color: #f1f5fa;
  cursor: pointer;
}

tbody td {
  vertical-align: middle;
}

.leaderboard-card {
  margin-top: 30px;
}
</style>
