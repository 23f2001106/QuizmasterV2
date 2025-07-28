<template>
  <div class="score-page">
    <SideBar />

    <main class="content">
      <div class="header">
        <h1 class="title">Quiz Attempts</h1>
        <button class="export-btn" @click="handleExport" :disabled="exporting">
          <ArrowDownTrayIcon class="icon" />
          <span>Export as CSV</span>
        </button>
      </div>

      <BaseLoader v-if="loading" />

      <div v-else>
        <BaseLoader v-if="exporting" />

        <BaseMessage
          v-if="exportStatus === 'pending'"
          type="info"
          message="Export in progress, please wait..."
        />

        <BaseMessage
          v-if="exportStatus === 'completed'"
          type="success"
          :message="'Export complete. You can now download the CSV.'"
        />
        <BaseMessage
          v-else-if="exportStatus === 'failed'"
          type="error"
          :message="exportErrorMsg || 'Export failed. Please try again.'"
        />

        <div v-if="downloadUrl" class="export-download text-center mb-4">
          <button class="btn btn-success" @click="downloadCSV">
            Download CSV
          </button>
        </div>
        <div v-if="scores.length === 0" class="text-center my-4">
          <BaseMessage type="warning" message="No quiz attempts found." />
        </div>
        <table v-else class="score-table">
          <thead>
            <tr>
              <th>S.No</th>
              <th>Quiz Name</th>
              <th>Score</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(score, index) in scores" :key="score.id">
              <td>{{ index + 1 }}</td>
              <td>{{ score.quiz_name }}</td>
              <td>{{ score.total_scored }} / {{ score.total_questions }}</td>
              <td>
                <button @click="openModal(score)">Details</button>
              </td>
            </tr>
          </tbody>
        </table>

        <div
          class="modal fade show"
          tabindex="-1"
          role="dialog"
          v-if="showModal"
          style="display: block; background: rgba(0, 0, 0, 0.5)"
        >
          <div class="modal-dialog modal-lg" role="document">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title">{{ selectedScore.quiz_name }}</h5>
                <button
                  type="button"
                  class="btn-close"
                  aria-label="Close"
                  @click="closeModal"
                ></button>
              </div>
              <div class="modal-body">
                <p>
                  <strong>Chapter:</strong> {{ selectedScore.chapter_name }}
                </p>
                <p>
                  <strong>Subject:</strong> {{ selectedScore.subject_name }}
                </p>
                <p>
                  <strong>Score:</strong>
                  {{ selectedScore.total_scored }} /
                  {{ selectedScore.total_questions }}
                </p>
                <p>
                  <strong>Time Taken:</strong>
                  {{ selectedScore.time_taken }} seconds
                </p>
                <p>
                  <strong>Date of Attempt:</strong>
                  {{ formatDate(selectedScore.time_stamp_of_attempt) }}
                </p>
              </div>
              <div class="modal-footer">
                <button class="btn btn-secondary" @click="closeModal">
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
  <AppFooter />
</template>

<script>
import axios from "axios";
import SideBar from "@/components/user/SideBar.vue";
import BaseLoader from "@/components/BaseLoader.vue";
import AppFooter from "@/components/AppFooter.vue";
import BaseMessage from "@/components/BaseMessage.vue";
import { ArrowDownTrayIcon } from "@heroicons/vue/24/outline";

export default {
  name: "ScorePage",

  components: {
    SideBar,
    BaseLoader,
    AppFooter,
    BaseMessage,
    ArrowDownTrayIcon,
  },

  data() {
    return {
      scores: [],
      loading: true,
      exporting: false,
      showModal: false,
      selectedScore: null,
      exportStatus: null,
      exportErrorMsg: null,
      downloadUrl: null,
      exportCheckInterval: null,
    };
  },

  methods: {
    async fetchScores() {
      this.loading = true;
      try {
        const res = await axios.get("/user/scores");
        this.scores = res.data.scores;
      } catch (err) {
        console.error("Failed to fetch scores:", err);
      } finally {
        this.loading = false;
      }
    },

    openModal(score) {
      this.selectedScore = score;
      this.showModal = true;
    },

    closeModal() {
      this.showModal = false;
      this.selectedScore = null;
    },

    formatDate(dateStr) {
      const date = new Date(dateStr);
      return date.toLocaleString();
    },
    async checkExportStatus() {
      try {
        const res = await axios.get("/user/export/status");
        if (res.data.status === "completed") {
          this.exportStatus = "completed";
          this.downloadUrl = res.data.download_url;
          this.exporting = false;
          clearInterval(this.exportCheckInterval);
          this.exportCheckInterval = null;
        } else if (res.data.status === "failed") {
          this.exportStatus = "failed";
          this.exporting = false;
          this.exportErrorMsg =
            res.data.message || "Export failed. Please try again.";
          clearInterval(this.exportCheckInterval);
          this.exportCheckInterval = null;
        } else if (res.data.status === "none") {
          this.exportStatus = null;
          this.exporting = false;
          clearInterval(this.exportCheckInterval);
          this.exportCheckInterval = null;
        } else {
          // Status is 'pending' or unknown — keep polling
          this.exportStatus = "pending";
        }
      } catch (err) {
        console.error("Failed to check export status:", err);
        this.exportStatus = "failed";
        this.exportErrorMsg = "Server error while checking export status.";
        this.exporting = false;
        if (this.exportCheckInterval) {
          clearInterval(this.exportCheckInterval);
          this.exportCheckInterval = null;
        }
      }
    },

    async handleExport() {
      try {
        this.exporting = true;
        this.exportStatus = null;
        this.exportErrorMsg = null;
        this.downloadUrl = null;

        await axios.post("/user/export");

        this.exportCheckInterval = setInterval(this.checkExportStatus, 5000);
      } catch (err) {
        console.error("Export failed:", err);
        this.exportStatus = "failed";
        this.exporting = false;
        this.exportErrorMsg = "Failed to start export.";
      }
    },
    async downloadCSV() {
      try {
        const res = await axios.get(this.downloadUrl, {
          responseType: "blob",
        });

        const blob = new Blob([res.data], { type: "text/csv" });
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.setAttribute("download", "quiz_scores.csv");
        document.body.appendChild(link);
        link.click();
        link.remove();
      } catch (err) {
        console.error("Download failed:", err);
      }
    },
  },

  mounted() {
    this.fetchScores();
  },
  beforeUnmount() {
    if (this.exportCheckInterval) {
      clearInterval(this.exportCheckInterval);
      this.exportCheckInterval = null;
    }
  },
};
</script>

<style scoped>
.score-page {
  display: flex;
}

.content {
  flex: 1;
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 10px;
  padding-bottom: 30px;
}

.export-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  background-color: #15ca85;
  color: white;
  padding: 8px 14px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
}

.export-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.export-btn:hover {
  background-color: #07955f;
}

.icon {
  width: 20px;
  height: 20px;
}

.export-download a {
  font-weight: 500;
  color: #10b981;
}

.title {
  font-size: 2rem;
  margin-bottom: 20px;
}

.score-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  background-color: #ffffff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.score-table thead {
  background-color: #eaf1fd;
}

.score-table th,
.score-table td {
  padding: 14px 16px;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
  font-size: 14px;
  color: #374151;
}

.score-table th {
  font-weight: 600;
  color: #111827;
}

.score-table tr:hover {
  background-color: #f9fafb;
}

.score-table tbody tr:last-child td {
  border-bottom: none;
}

.score-table button {
  padding: 6px 12px;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.score-table button:hover {
  background-color: #2563eb;
}
</style>
