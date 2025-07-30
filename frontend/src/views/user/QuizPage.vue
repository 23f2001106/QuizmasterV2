<template>
  <div class="quiz-page d-flex flex-column min-vh-100">
    <div class="d-flex flex-grow-1">
      <div class="sidebar bg-light">
        <SideBar />
      </div>

      <div class="flex-grow-1 p-4">
        <h2 class="mb-4">Available Quizzes</h2>

        <div class="mb-1 row">
          <div class="col-md-12">
            <select v-model="sortField" class="form-select">
              <option disabled value="">Sort by</option>
              <option value="name">Name</option>
              <option value="date_of_quiz">Date of Quiz</option>
              <option value="due_date">Due Date</option>
            </select>
          </div>
        </div>
        <div class="mb-3 text-end">
          <button class="btn btn-sm btn-secondary" @click="toggleSortDirection">
            Sort: {{ sortDirection === "asc" ? "Ascending" : "Descending" }}
          </button>
        </div>

        <BaseLoader v-if="loading" />

        <div v-else-if="filteredQuizzes.length === 0" class="alert alert-info">
          No quizzes available.
        </div>

        <!-- Quiz Table -->
        <div v-else>
          <table class="available-quiz-table">
            <thead>
              <tr>
                <th>S No.</th>
                <th>Quiz Name</th>
                <th style="width: 100px">View</th>
                <th style="width: 100px">Start</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(quiz, index) in filteredQuizzes" :key="quiz.id">
                <td>{{ index + 1 }}</td>
                <td>{{ quiz.name }}</td>
                <td>
                  <button
                    class="btn view btn-sm btn-outline-info"
                    @click="viewQuiz(quiz)"
                  >
                    View
                  </button>
                </td>
                <td>
                  <button
                    class="btn start btn-sm btn-primary"
                    @click="startQuiz(quiz.id)"
                  >
                    Start
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Modal for Quiz Details -->
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
                <p><strong>Chapter:</strong> {{ selectedQuiz.chapter_name }}</p>
                <p><strong>Subject:</strong> {{ selectedQuiz.subject_name }}</p>
                <p>
                  <strong>Date of Quiz:</strong>
                  {{ formatDateTime(selectedQuiz.date_of_quiz) }}
                </p>
                <p>
                  <strong>Due Date:</strong>
                  {{ formatDateTime(selectedQuiz.due_date) }}
                </p>
                <p>
                  <strong>Time Duration:</strong>
                  {{ formatDuration(selectedQuiz.time_duration) }}
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
    </div>

    <AppFooter />
  </div>
</template>

<script>
import axios from "axios";
import SideBar from "@/components/user/SideBar.vue";
import AppFooter from "@/components/AppFooter.vue";
import BaseLoader from "@/components/BaseLoader.vue";

export default {
  name: "QuizPage",
  components: {
    SideBar,
    AppFooter,
    BaseLoader,
  },
  data() {
    return {
      quizzes: [],
      selectedQuiz: null,
      loading: true,
      filters: {
        name: "",
        date_of_quiz: "",
        due_date: "",
      },
      sortField: "",
      sortDirection: "asc",
    };
  },
  computed: {
    filteredQuizzes() {
      let result = this.quizzes;
      // Sort
      if (this.sortField) {
        result = [...result].sort((a, b) => {
          const valA = a[this.sortField];
          const valB = b[this.sortField];

          if (valA < valB) return this.sortDirection === "asc" ? -1 : 1;
          if (valA > valB) return this.sortDirection === "asc" ? 1 : -1;
          return 0;
        });
      }

      return result;
    },
  },
  methods: {
    async fetchQuizzes() {
      try {
        const res = await axios.get("/user/quizzes");
        console.log("Quiz response:", res.data);
        this.quizzes = res.data.map((q) => ({
          id: q.id,
          name: q.name,
          chapter_name: q.chapter_name,
          subject_name: q.subject_name,
          date_of_quiz: q.date_of_quiz,
          due_date: q.due_date,
          time_duration: q.time_duration,
          remarks: q.remarks,
        }));
      } catch (err) {
        console.error("Failed to fetch quizzes:", err);
      } finally {
        this.loading = false;
      }
    },
    formatDateTime(datetimeStr) {
      return datetimeStr || "N/A";
    },
    formatDuration(durationStr) {
      const [h, m, s] = durationStr.split(":");
      return `${parseInt(h)}h ${parseInt(m)}m ${parseInt(s)}s`;
    },
    viewQuiz(quiz) {
      this.selectedQuiz = quiz;
    },
    startQuiz(quizId) {
      this.$router.push({ name: "TakeQuiz", params: { quizId } });
    },
    toggleSortDirection() {
      this.sortDirection = this.sortDirection === "asc" ? "desc" : "asc";
    },
  },
  mounted() {
    this.fetchQuizzes();
  },
};
</script>

<style scoped>
.quiz-page {
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f9fafb;
  color: #333;
  min-height: 100vh;
}

.flex-grow-1.p-4 {
  background-color: #fff;
  border-radius: 0 8px 8px 0;
  padding: 2rem 2.5rem;
  box-shadow: inset 0 0 12px rgb(0 0 0 / 0.03);
  overflow-x: auto;
}

h2 {
  font-weight: 700;
  color: #2c3e50;
  padding-bottom: 40px;
}

select.form-select {
  border: 1.5px solid #ced4da;
  border-radius: 6px;
  padding: 0.375rem 0.75rem;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

select.form-select:focus {
  border-color: #6c757d;
  outline: none;
  box-shadow: 0 0 5px rgba(108, 117, 125, 0.5);
}

.btn-sm.btn-secondary {
  margin-top: 20px;
  background-color: #0ac0d8;
  border-color: transparent;
  color: #fff;
  border-radius: 6px;
  font-weight: 600;
  transition: background-color 0.3s ease;
}

.btn-sm.btn-secondary:hover {
  background-color: #fff;
  border-color: #0ac0d8;
  color: #0ac0d8;
}

.available-quiz-table {
  width: 100%;
  margin: 20px 0;
  border-collapse: collapse;
  background-color: #f9f9f9;
  border-radius: 8px;
  overflow: hidden;
}

.available-quiz-table thead {
  background-color: #4adbca;
  color: #314a67;
}

.available-quiz-table th {
  padding: 12px !important;
  font-size: 1rem;
  text-align: left;
  border-bottom: 1px solid #dee2e6;
}

.available-quiz-table td {
  padding: 12px !important;
  font-size: 1rem;
  color: #333;
}

.available-quiz-table tbody tr:hover {
  background-color: #dfdede;
}

.alert-info {
  background-color: #e7f3fe;
  color: #31708f;
  border: 1px solid #bce8f1;
  border-radius: 6px;
  padding: 1rem 1.25rem;
  font-size: 1.1rem;
}

.btn-sm {
  border-radius: 6px;
  font-weight: 600;
  transition: background-color 0.3s ease, color 0.3s ease;
  padding: 0.375rem 0.75rem;
  font-size: 0.85rem;
  box-shadow: none;
}

.btn-outline-info {
  color: #17a2b8;
  border-color: #17a2b8;
}

.btn-outline-info:hover {
  background-color: #17a2b8;
  color: #fff;
}

.btn-primary {
  background-color: #3294fd;
  border-color: none;
  color: #fff;
}

.btn-primary:hover {
  background-color: #0056b3;
  border-color: none;
  color: #fff;
}

.btn-close {
  border: none;
  background: transparent;
  font-size: 1.25rem;
  cursor: pointer;
  opacity: 0.6;
  transition: opacity 0.3s ease;
}

.btn-close:hover {
  opacity: 1;
}

@media (max-width: 576px) {
  .flex-grow-1.p-4 {
    padding: 1rem 1.25rem;
  }

  table.table thead {
    display: none;
  }

  table.table tbody tr {
    display: block;
    margin-bottom: 1rem;
    box-shadow: none;
    background: #fff;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    padding: 1rem;
  }

  table.table tbody td {
    display: flex;
    justify-content: space-between;
    padding: 0.5rem 0;
    border: none;
  }

  table.table tbody td::before {
    content: attr(data-label);
    font-weight: 600;
    color: #6c757d;
  }

  table.table tbody td:nth-child(1),
  table.table tbody td:nth-child(2),
  table.table tbody td:nth-child(3),
  table.table tbody td:nth-child(4) {
    width: 100%;
  }

  .btn-sm {
    width: 48%;
    margin-bottom: 0.5rem;
  }

  .btn-sm:last-child {
    margin-bottom: 0;
  }
}
</style>
