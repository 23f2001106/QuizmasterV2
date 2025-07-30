<template>
  <div class="summary-layout">
    <SideBar />

    <div class="main-content">
      <BaseLoader v-if="loading" />

      <div v-else>
        <header class="summary-header">
          <h2>Welcome, {{ summary.full_name }}</h2>
        </header>

        <!-- Charts -->
        <section class="charts">
          <div class="chart-card">
            <h3>Score Trend</h3>
            <LineChart
              v-if="summary.score_trend.length"
              :data="
                summary.score_trend.map((s) => ({
                  date: s.date,
                  value: s.score,
                }))
              "
            />
            <p v-else>No score trend data.</p>
          </div>
          <div class="chart-card">
            <h3>Score Distribution</h3>
            <PieChart
              v-if="summary.score_distribution"
              :data="summary.score_distribution"
            />
            <p v-else>No scores.</p>
          </div>
          <div class="chart-card">
            <h3>Subject Performance</h3>
            <BarChart
              v-if="summary.subject_performance.length"
              :labels="summary.subject_performance.map((s) => s.label)"
              :values="summary.subject_performance.map((s) => s.value)"
              label="Avg Score"
              :colors="['#a3cef1', '#fcd5ce', '#cdb4db', '#b5ead7', '#f9dc5c']"
            />
            <p v-else>No subject performance data.</p>
          </div>
        </section>

        <!-- Key Stats Cards -->
        <section class="key-stats">
          <div class="stat-card">
            <div class="card-body">
              <div class="card-title">Best Subject</div>
              <div>{{ summary.best_subject || "N/A" }}</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="card-body">
              <div class="card-title">Weak Subject</div>
              <div>{{ summary.weak_subject || "N/A" }}</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="card-body">
              <div class="card-title">Most Attempted Subject</div>
              <div>{{ summary.most_attempted_subject || "N/A" }}</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="card-body">
              <div class="card-title">Avg Time/Quiz (s)</div>
              <div>{{ summary.average_time_per_quiz }}</div>
            </div>
          </div>
        </section>

        <!-- Attempts per Subject & Weekly Attempts -->
        <section class="charts">
          <div class="chart-card">
            <h3>Attempts per Subject</h3>
            <BarChart
              v-if="summary.attempts_per_subject.length"
              :labels="summary.attempts_per_subject.map((s) => s.label)"
              :values="summary.attempts_per_subject.map((s) => s.value)"
              label="Attempts"
              :colors="[
                '#66bb6a',
                '#42a5f5',
                '#ffa726',
                '#ab47bc',
                '#29b6f6',
                '#ef5350',
              ]"
            />
            <p v-else>No data.</p>
          </div>
          <div class="chart-card">
            <h3>Weekly Attempts</h3>
            <BarChart
              v-if="summary.weekly_attempts.length"
              :labels="summary.weekly_attempts.map((w) => w.date)"
              :values="summary.weekly_attempts.map((w) => w.value)"
              label="Attempts"
              :colors="[
                '#4adbca',
                '#ff595e',
                '#1982c4',
                '#6a4c93',
                '#8ac926',
                '#ffca3a',
              ]"
            />
            <p v-else>No weekly data.</p>
          </div>
        </section>

        <!-- Leaderboard -->
        <section class="leaderboard-card">
          <h3>Leaderboard</h3>
          <table v-if="summary.leaderboard.length">
            <thead>
              <tr>
                <th>Rank</th>
                <th>User</th>
                <th>Avg Score</th>
                <th>Attempts</th>
              </tr>
            </thead>
            <tbody>
              <!-- Top 5 performers -->
              <tr
                v-for="u in topPerformers"
                :key="u.rank"
                :class="{ you: u.is_you }"
              >
                <td>{{ u.rank }}</td>
                <td>{{ u.user }} <span v-if="u.is_you">(You)</span></td>
                <td>{{ u.average_score }}%</td>
                <td>{{ u.quizzes_attempted }}</td>
              </tr>

              <!-- Divider row -->
              <tr v-if="extraUser" class="divider-row">
                <td colspan="4" style="text-align: center; font-weight: 600">
                  Your Rank
                </td>
              </tr>

              <!-- Current user's separate rank (if not in top) -->
              <tr v-if="extraUser" class="you">
                <td>{{ extraUser.rank }}</td>
                <td>{{ extraUser.user }} <span>(You)</span></td>
                <td>{{ extraUser.average_score }}%</td>
                <td>{{ extraUser.quizzes_attempted }}</td>
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
import SideBar from "@/components/user/SideBar.vue";
import AppFooter from "@/components/AppFooter.vue";
import BaseLoader from "@/components/BaseLoader.vue";
import LineChart from "@/components/charts/LineChart.vue";
import PieChart from "@/components/charts/PieChart.vue";
import BarChart from "@/components/charts/BarChart.vue";

export default {
  name: "UserSummary",
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
      summary: null,
      loading: true,
    };
  },
  computed: {
    topPerformers() {
      const leaderboard = this.summary?.leaderboard || [];
      const top5 = leaderboard.slice(0, 5);
      return top5;
    },
    extraUser() {
      const leaderboard = this.summary?.leaderboard || [];
      const top5 = leaderboard.slice(0, 5);
      const isUserInTop5 = top5.some((entry) => entry.is_you);

      if (!isUserInTop5 && leaderboard.length > 5) {
        return leaderboard[leaderboard.length - 1];
      }
      return null;
    },
  },
  mounted() {
    this.fetchSummary();
  },
  methods: {
    async fetchSummary() {
      try {
        const res = await axios.get("/user/summary");
        console.log("API Response:", res.data);
        this.summary = res.data;
      } catch (err) {
        console.error("Failed to load summary:", err);
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

.charts {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
}
.chart-card,
.leaderboard-card {
  flex: 1;
  background: #fff;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 1.5rem;
}
.key-stats {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1.5rem;
}
.stat-card {
  flex: 1;
  min-width: 150px;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
  background: #fff;
}
.stat-card:hover {
  transform: scale(1.03);
}
.stat-card .card-body {
  padding: 1rem;
  text-align: center;
}
.card-title {
  font-weight: 600;
  color: #314a67;
  margin-bottom: 0.5rem;
}
.leaderboard-card table {
  width: 100%;
  border-collapse: collapse;
}
.leaderboard-card th,
.leaderboard-card td {
  padding: 0.75rem;
  border-bottom: 1px solid #eee;
}
.leaderboard-card tr.you {
  background-color: #e0f7fa;
}
.leaderboard-card tr:hover {
  background: #f5f5f5;
}
.leaderboard-card .you {
  background-color: #e0f7fa;
  font-weight: 600;
}

.divider-row td {
  border-top: 2px solid #999;
  background-color: #f0f0f0;
}
</style>
