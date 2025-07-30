<template>
  <div class="page-layout">
    <SideBar />

    <div class="main-content">
      <BaseLoader v-if="loading" />

      <div v-else>
        <header class="page-header">
          <h2>Welcome, Admin</h2>
        </header>

        <!-- Search Form -->
        <form @submit.prevent="handleSearch">
          <div class="mb-3">
            <label for="category-select" class="form-label">Category</label>
            <select
              id="category-select"
              v-model="form.category"
              class="form-select"
              required
              :class="{ 'text-muted': form.category === '' }"
            >
              <option disabled value="" selected hidden>Category</option>
              <option value="users">Users</option>
              <option value="subjects">Subjects</option>
              <option value="quizzes">Quizzes</option>
            </select>
          </div>

          <div class="mb-3">
            <input
              type="text"
              id="search-input"
              v-model="form.query"
              class="form-control"
              placeholder="Enter name to search..."
            />
          </div>

          <div class="text-center">
            <button type="submit" class="btn btn-outline-primary">
              Search
            </button>
          </div>
        </form>

        <!-- Search Results -->
        <div class="mt-4" v-if="results.length">
          <h5>Search Results</h5>
          <table class="result-table">
            <thead>
              <tr>
                <th v-for="header in tableHeaders" :key="header">
                  {{ header }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in results" :key="item.id">
                <td v-for="header in tableHeaders" :key="header">
                  {{ formatCell(item, header) }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-else-if="searched">
          <p>No results found.</p>
        </div>
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
import { useToast } from "vue-toastification";

export default {
  name: "SearchPage",
  components: {
    SideBar,
    AppFooter,
    BaseLoader,
  },
  data() {
    return {
      loading: false,
      searched: false,
      form: {
        category: "",
        query: "",
      },
      results: [],
      toast: useToast(),
    };
  },
  computed: {
    tableHeaders() {
      if (!this.results.length) return [];

      const firstItem = this.results[0];
      return Object.keys(firstItem).map((key) =>
        key === "question count" ? "question_count" : key
      );
    },
  },
  methods: {
    async handleSearch() {
      this.loading = true;
      this.results = [];
      this.searched = false;

      if (!this.form.query.trim()) {
        this.toast.warning("Please enter a search query");
        this.loading = false;
        return;
      }

      try {
        const response = await axios.get("/admin/search", {
          params: {
            category: this.form.category,
            query: this.form.query,
          },
        });

        this.results = response.data.results || [];
        this.searched = true;
      } catch (error) {
        console.error("Search failed:", error);
        this.toast.error("Error fetching search results");
      } finally {
        this.loading = false;
      }
    },
    formatCell(item, key) {
      const normalizedKey = key.replace(/\s+/g, "_").toLowerCase();
      return item[key] ?? item[normalizedKey] ?? "-";
    },
  },
};
</script>

<style scoped>
.page-layout {
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

.page-header {
  margin-bottom: 2rem;
  font-size: 1.5rem;
  font-weight: 600;
}

.result-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  margin-top: 20px;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  font-size: 15px;
}

.result-table thead {
  background-color: #eff6ff;
}

.result-table th {
  padding: 16px;
  text-align: center;
  font-weight: 600;
  color: #1e3a8a;
  border-bottom: 1px solid #d1d5db;
}

.result-table td {
  padding: 16px;
  text-align: center;
  color: #374151;
  border-bottom: 1px solid #f3f4f6;
  background-color: #fff;
}

.result-table tbody tr:nth-child(even) td {
  background-color: #f9fafb;
}

.result-table tbody tr:hover td {
  background-color: #e0f3f7 !important;
  transition: background-color 0.2s ease-in-out;
}
</style>
