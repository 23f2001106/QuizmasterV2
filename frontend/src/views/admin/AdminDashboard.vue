<template>
  <div class="dashboard-layout">
    <SideBar />

    <div class="main-content">
      <!-- Loader -->
      <BaseLoader v-if="loading" />

      <div v-else>
        <!-- Welcome -->
        <header class="dashboard-header">
          <h2>Welcome, Admin</h2>
          <router-link
            to="/admin/search"
            class="search-button btn btn-outline-primary d-flex align-items-center ms-auto"
            @click="onSearchClick"
          >
            <MagnifyingGlassIcon class="me-2 icon" />
            <span>Search</span>
          </router-link>
        </header>

        <!-- STAT CARDS -->
        <section class="key-stats">
          <div
            class="stat-card"
            v-for="(value, key) in dashboard.stats"
            :key="key"
          >
            <div class="card-body">
              <div class="card-title">{{ formatTitle(key) }}</div>
              <div class="card-text">{{ value }}</div>
            </div>
          </div>
        </section>

        <!-- ALERTS -->
        <section class="alerts">
          <h3>Alerts</h3>
          <ul>
            <li>
              Unverified Users: {{ dashboard.alerts?.unverified_users || 0 }}
            </li>
            <li>
              Subjects Without Chapters:
              {{ dashboard.alerts?.subjects_without_chapters || 0 }}
            </li>
            <li>
              Chapters Without Quizzes:
              {{ dashboard.alerts?.chapters_without_quizzes || 0 }}
            </li>
            <li>
              Past Due Quizzes: {{ dashboard.alerts?.quizzes_past_due || 0 }}
            </li>
          </ul>
        </section>

        <!-- TABLES -->
        <section class="tables">
          <!-- Recent Users -->
          <div class="table-card">
            <h3>Recent Users</h3>
            <table v-if="dashboard.recent_users.length">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Username</th>
                  <th>Created At</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="user in dashboard.recent_users" :key="user.id">
                  <td>{{ user.full_name }}</td>
                  <td>{{ user.username }}</td>
                  <td>{{ formatDate(user.created_at) }}</td>
                </tr>
              </tbody>
            </table>
            <p v-else>No recent users.</p>
          </div>

          <!-- Recent Quizzes -->
          <div class="table-card">
            <h3>Recent Quizzes</h3>
            <table v-if="dashboard.recent_quizzes.length">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Subject</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="quiz in dashboard.recent_quizzes" :key="quiz.id">
                  <td>{{ quiz.name }}</td>
                  <td>{{ quiz.subject }}</td>
                  <td>{{ formatDate(quiz.date_of_quiz) }}</td>
                </tr>
              </tbody>
            </table>
            <p v-else>No recent quizzes.</p>
          </div>

          <!-- Upcoming Quizzes -->
          <div class="table-card">
            <h3>Upcoming Quizzes</h3>
            <table v-if="dashboard.upcoming_quizzes.length">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Subject</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="quiz in dashboard.upcoming_quizzes" :key="quiz.id">
                  <td>{{ quiz.name }}</td>
                  <td>{{ quiz.subject }}</td>
                  <td>{{ formatDate(quiz.date_of_quiz) }}</td>
                </tr>
              </tbody>
            </table>
            <p v-else>No upcoming quizzes.</p>
          </div>
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
import { MagnifyingGlassIcon } from "@heroicons/vue/24/outline";

export default {
  name: "AdminDashboard",
  components: {
    SideBar,
    AppFooter,
    BaseLoader,
    MagnifyingGlassIcon,
  },
  data() {
    return {
      dashboard: {
        stats: {},
        alerts: {},
        recent_users: [],
        recent_quizzes: [],
        upcoming_quizzes: [],
      },
      loading: true,
    };
  },
  mounted() {
    this.fetchDashboard();
  },
  methods: {
    async fetchDashboard() {
      try {
        const res = await axios.get("/admin/dashboard");
        this.dashboard = res.data;
      } catch (err) {
        console.error("Error loading dashboard:", err);
      } finally {
        this.loading = false;
      }
    },
    formatDate(dateStr) {
      const d = new Date(dateStr);
      return `${d.getDate().toString().padStart(2, "0")}/${(d.getMonth() + 1)
        .toString()
        .padStart(2, "0")}/${d.getFullYear()}`;
    },
    formatTitle(key) {
      return key.replace(/_/g, " ").replace(/\b\w/g, (l) => l.toUpperCase());
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
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.dashboard-header h2 {
  font-size: 1.75rem;
  font-weight: 600;
}

.icon {
  width: 20px;
  height: 20px;
}

.key-stats {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1rem;
  text-align: center;
  background: #fff;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}

.card-title {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.card-text {
  font-size: 1.4rem;
  font-weight: 500;
  color: #4adbca;
}

.alerts {
  margin-bottom: 2rem;
}

.alerts ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.alerts li {
  background: #fff5f5;
  border-left: 4px solid #f44336;
  padding: 0.75rem;
  margin-bottom: 0.5rem;
  border-radius: 4px;
  transition: background-color 0.3s ease;
}

.alerts li:hover {
  background-color: #ffe9e9;
}

.tables {
  display: grid;
  gap: 2rem;
}

.table-card {
  background: #fff;
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.table-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 10px rgba(0, 0, 0, 0.08);
}
.table-card h3 {
  margin-bottom: 1rem;
}

.table-card table {
  width: 100%;
  border-collapse: collapse;
}

.table-card th,
.table-card td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.table-card tbody tr:hover {
  background-color: #f2f9f9;
  transition: background-color 0.2s ease;
}
</style>
