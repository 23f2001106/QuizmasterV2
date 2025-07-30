<template>
  <div class="dashboard-layout">
    <SideBar />

    <div class="main-content">
      <BaseLoader v-if="loading" />

      <div v-else>
        <header class="dashboard-header">
          <h2>Welcome, {{ dashboard.full_name }}</h2>
        </header>

        <div class="stats-cards">
          <div class="stat-card">
            <div class="card-body">
              <div class="card-title">Total Quizzes Attempted</div>
              <div class="card-text">
                {{ dashboard.total_quizzes_attempted }}
              </div>
            </div>
          </div>
          <div class="stat-card">
            <div class="card-body">
              <div class="card-title">Average Score</div>
              <div class="card-text">{{ dashboard.average_score }}%</div>
            </div>
          </div>
        </div>

        <div class="last-quiz" v-if="dashboard.last_quiz">
          <h3 class="card-title">Last Quiz Summary</h3>
          <div class="stat-card">
            <div class="card-body">
              <p><strong>Quiz:</strong> {{ dashboard.last_quiz.quiz_name }}</p>
              <p><strong>Score:</strong> {{ dashboard.last_quiz.score }}%</p>
              <p>
                <strong>Date:</strong>
                {{ formatDate(dashboard.last_quiz.date) }}
              </p>
            </div>
          </div>
        </div>

        <div class="upcoming-quizzes">
          <h3 class="card-title">Upcoming Quizzes</h3>
          <table
            v-if="dashboard.upcoming_quizzes.length"
            class="Upcoming-quiz-table"
          >
            <thead>
              <tr>
                <th>Name</th>
                <th>Subject</th>
                <th>Due Date</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="quiz in dashboard.upcoming_quizzes" :key="quiz.id">
                <td>{{ quiz.name }}</td>
                <td>{{ quiz.subject }}</td>
                <td>{{ formatDate(quiz.due_date) }}</td>
                <td>
                  <button @click="viewQuizDetails(quiz)">View</button>
                </td>
              </tr>
            </tbody>
          </table>
          <p v-else>No upcoming quizzes.</p>
        </div>

        <div class="performance-chart">
          <h3>Performance Breakdown</h3>
          <div v-if="hasPerformanceData">
            <PieChart :data="dashboard.performance_breakdown" />
          </div>
          <p v-else>No performance data to display.</p>
        </div>
      </div>
    </div>

    <!-- Quiz Details Modal -->
    <div
      class="modal fade show"
      tabindex="-1"
      role="dialog"
      v-if="selectedQuiz"
      style="display: block; background: rgba(0, 0, 0, 0.5)"
    >
      <div class="modal-dialog modal-lg" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ selectedQuiz.name }}</h5>
            <button
              type="button"
              class="btn-close"
              @click="selectedQuiz = null"
            ></button>
          </div>
          <div class="modal-body">
            <p><strong>Subject:</strong> {{ selectedQuiz.subject }}</p>
            <p>
              <strong>Date of Quiz:</strong>
              {{ formatDate(selectedQuiz.date_of_quiz) }}
            </p>
            <p>
              <strong>Due Date:</strong>
              {{ formatDate(selectedQuiz.due_date) }}
            </p>
            <p>
              <strong>Time Duration:</strong>
              {{ selectedQuiz.time_duration }}
            </p>
            <p v-if="selectedQuiz.remarks">
              <strong>Remarks:</strong> {{ selectedQuiz.remarks }}
            </p>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="selectedQuiz = null">
              Close
            </button>
          </div>
        </div>
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
import PieChart from "@/components/charts/PieChart.vue";

export default {
  name: "UserDashboard",
  components: {
    SideBar,
    AppFooter,
    BaseLoader,
    PieChart,
  },
  data() {
    return {
      dashboard: null,
      loading: true,
      selectedQuiz: null,
    };
  },
  computed: {
    hasPerformanceData() {
      const breakdown = this.dashboard?.performance_breakdown;
      return (
        breakdown &&
        (breakdown.high > 0 || breakdown.moderate > 0 || breakdown.low > 0)
      );
    },
  },
  mounted() {
    this.fetchDashboard();
  },
  methods: {
    async fetchDashboard() {
      try {
        const res = await axios.get("/user/dashboard");
        console.log(res.data);
        this.dashboard = res.data;
      } catch (err) {
        console.error("Failed to load dashboard:", err);
      } finally {
        this.loading = false;
      }
    },
    viewQuizDetails(quiz) {
      console.log("Quiz clicked:", quiz);
      this.selectedQuiz = quiz;
    },
    formatDate(dateStr) {
      if (!dateStr || typeof dateStr !== "string") return "N/A";

      const parsedDate = new Date(dateStr);
      if (isNaN(parsedDate.getTime())) return "N/A";

      const options = { year: "numeric", month: "long", day: "numeric" };
      return parsedDate.toLocaleDateString(undefined, options);
    },
  },
};
</script>

<style scoped>
.dashboard-layout {
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

.dashboard-header {
  margin-bottom: 2rem;
  font-size: 1.5rem;
  font-weight: 600;
}

.stat-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
  transition: transform 0.3s ease;
  background-color: #fff;
  flex: 1;
  margin-right: 20px;
}

.stat-card:last-child {
  margin-right: 0;
}

.stat-card:hover {
  transform: scale(1.05);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
}

.stat-card .card-body {
  text-align: center;
  padding: 20px;
}

.card-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #314a67;
  margin-bottom: 10px;
}

.card-text {
  font-size: 1.5rem;
  font-weight: 500;
  color: #222;
}

.stats-cards {
  display: flex;
  flex-wrap: wrap;
  margin-bottom: 2rem;
}
.last-quiz {
  margin-bottom: 2rem;
}

.Upcoming-quiz-table {
  width: 100%;
  margin: 20px 0;
  border-collapse: collapse;
  background-color: #f9f9f9;
  border-radius: 8px;
  overflow: hidden;
}

.Upcoming-quiz-table thead {
  background-color: #4adbca;
  color: #314a67;
}

.Upcoming-quiz-table th {
  padding: 12px;
  font-size: 1rem;
  text-align: left;
}

.Upcoming-quiz-table td {
  padding: 12px;
  font-size: 1rem;
  color: #333;
}

.Upcoming-quiz-table tbody tr:hover {
  background-color: #dfdede;
}

.performance-chart {
  max-width: 400px;
  margin-top: 2rem;
}

button {
  padding: 0.5rem 1rem;
  background-color: #4adbca;
  color: #314a67;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
}

button:hover {
  background-color: #40c8b8;
}
</style>
