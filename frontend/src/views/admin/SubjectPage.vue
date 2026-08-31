<template>
  <div class="page-layout">
    <SideBar />

    <div class="main-content">
      <BaseLoader v-if="loading" />

      <div v-else>
        <header class="page-header">
          <h2>Welcome, Admin</h2>
        </header>

        <h4 class="section-title p-4">Subjects</h4>
        <div class="text-center mt-4 mb-4">
          <button class="btn btn-special" @click="openSubjectModal('add')">
            Add Subject
          </button>
        </div>
        <div class="row">
          <template v-if="subjects.length">
            <div
              v-for="subject in subjects"
              :key="subject.id"
              class="col-md-6 mb-3"
            >
              <div class="card">
                <div class="card-header">
                  <h5>{{ subject.name }}</h5>
                </div>
                <div class="card-body">
                  <table
                    v-if="subject.chapters.length"
                    class="table table-bordered subject-table"
                  >
                    <thead>
                      <tr>
                        <th>ID</th>
                        <th>Chapter Name</th>
                        <th>Action</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="chapter in subject.chapters" :key="chapter.id">
                        <td>{{ chapter.id }}</td>
                        <td>{{ chapter.name }}</td>
                        <td>
                          <button
                            class="btn btn-primary btn-sm"
                            @click="viewChapter(chapter)"
                          >
                            View
                          </button>
                          <button
                            class="btn btn-warning btn-sm"
                            @click="editChapter(chapter, subject.id)"
                          >
                            Edit
                          </button>
                          <button
                            class="btn btn-danger btn-sm"
                            @click="deleteChapter(chapter.id)"
                          >
                            Delete
                          </button>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                  <p v-else class="text-center text-muted no-chapters-msg">
                    No chapters available
                  </p>

                  <button
                    class="btn btn-success btn-sm"
                    @click="addChapter(subject.id)"
                  >
                    Add Chapter
                  </button>

                  <div class="mt-3 text-center">
                    <button
                      class="btn btn-primary btn-sm"
                      @click="openSubjectModal('view', subject)"
                    >
                      View Subject
                    </button>
                    <button
                      class="btn btn-warning btn-sm"
                      @click="openSubjectModal('edit', subject)"
                    >
                      Edit Subject
                    </button>
                    <button
                      class="btn btn-danger btn-sm"
                      @click="deleteSubject(subject.id)"
                    >
                      Delete Subject
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </template>
          <p v-else class="text-center text-muted w-100 p-4">
            No subjects found. Click "Add Subject" to create one.
          </p>
        </div>
      </div>
    </div>
  </div>
  <AppFooter />

  <FormModal
    v-if="showModal"
    :title="modalTitle"
    :formData="modalData"
    :fields="modalFields"
    :readOnly="modalReadOnly"
    @close="showModal = false"
    @form-submit="handleSubjectSubmit"
  />
  <ConfirmModal
    v-if="confirmModal.show"
    :title="confirmModal.title"
    :message="confirmModal.message"
    @confirm="handleConfirm"
    @cancel="handleCancel"
  />
</template>

<script>
import SideBar from "@/components/admin/SideBar.vue";
import AppFooter from "@/components/AppFooter.vue";
import BaseLoader from "@/components/BaseLoader.vue";
import FormModal from "@/components/admin/FormModal.vue";
import ConfirmModal from "@/components/ConfirmModal.vue";
import axios from "axios";
import { useToast } from "vue-toastification";

export default {
  name: "SubjectPage",
  components: {
    SideBar,
    AppFooter,
    BaseLoader,
    FormModal,
    ConfirmModal,
  },
  data() {
    return {
      loading: true,
      subjects: [],
      showModal: false,
      modalTitle: "",
      modalFields: [],
      modalData: {},
      modalReadOnly: false,
      modalAction: null,
      currentSubjectId: null,
      confirmModal: {
        show: false,
        title: "Please Confirm",
        message: "",
        onConfirm: null,
      },
    };
  },
  mounted() {
    this.fetchSubjects();
  },
  methods: {
    openConfirmModal(message, onConfirm) {
      this.confirmModal.message = message;
      this.confirmModal.onConfirm = onConfirm;
      this.confirmModal.show = true;
    },
    handleConfirm() {
      if (typeof this.confirmModal.onConfirm === "function") {
        this.confirmModal.onConfirm();
      }
      this.confirmModal.show = false;
    },
    handleCancel() {
      this.confirmModal.show = false;
    },
    async fetchSubjects() {
      try {
        this.loading = true;
        const res = await axios.get("/admin/subjects");
        this.subjects = res.data;
      } catch (e) {
        console.error("Failed to fetch subjects:", e);
      } finally {
        this.loading = false;
      }
    },
    openSubjectModal(mode, subject = {}) {
      this.modalTitle =
        mode === "add"
          ? "Add Subject"
          : mode === "edit"
          ? "Edit Subject"
          : "View Subject";
      this.modalFields = [
        { name: "name", label: "Name", type: "text" },
        { name: "level", label: "Level", type: "text", required: false },
        {
          name: "description",
          label: "Description",
          type: "textarea",
          required: false,
        },
      ];
      if (mode === "add") {
        this.modalData = {
          name: "",
          level: "",
          description: "",
        };
      } else {
        this.modalData = { ...subject };
      }
      this.modalReadOnly = mode === "view";
      this.modalAction = mode;
      this.showModal = true;
    },
    async handleSubjectSubmit(data) {
      console.log("Submitting subject data:", data);
      const toast = useToast();
      try {
        if (!data.name?.trim()) {
          toast.error("Subject name is required.");
          return;
        }
        if (this.modalAction === "add") {
          await axios.post("/admin/subjects", data);
          console.log("Subject added:", data);
          toast.success("Subject added successfully");
        } else if (this.modalAction === "edit") {
          if (!data.id) {
            toast.error("Missing subject ID.");
            return;
          }
          await axios.put(`/admin/subjects/${data.id}`, data);
          toast.success("Subject updated successfully");
        } else if (this.modalAction === "add-chapter") {
          await axios.post(
            `/admin/subjects/${this.currentSubjectId}/chapters`,
            data
          );
          toast.success("Chapter added successfully");
        } else if (this.modalAction === "edit-chapter") {
          await axios.put(`/admin/chapters/${data.id}`, data);
          toast.success("Chapter updated successfully");
        }
        this.fetchSubjects();
      } catch (e) {
        toast.error("An error occured");
        console.error("Form submission error:", e);
      } finally {
        this.showModal = false;
      }
    },
    async deleteSubject(subjectId) {
      this.openConfirmModal(
        "Are you sure you want to delete this subject?",
        async () => {
          const toast = useToast();
          try {
            await axios.delete(`/admin/subjects/${subjectId}`);
            toast.success("Subject deleted successfully.");
            this.fetchSubjects();
          } catch (e) {
            console.error("Failed to delete subject:", e);
            toast.error("Failed to delete subject.");
          }
        }
      );
    },
    addChapter(subjectId) {
      this.currentSubjectId = subjectId;
      this.modalTitle = "Add Chapter";
      this.modalFields = [
        { name: "name", label: "Name", type: "text" },
        {
          name: "description",
          label: "Description",
          type: "textarea",
          required: false,
        },
      ];
      this.modalData = {};
      this.modalReadOnly = false;
      this.modalAction = "add-chapter";
      this.showModal = true;
    },
    viewChapter(chapter) {
      this.modalTitle = "View Chapter";
      this.modalFields = [
        { name: "id", label: "ID", type: "number", disabled: true },
        { name: "name", label: "Name", type: "text", disabled: true },
        {
          name: "description",
          label: "Description",
          type: "textarea",
          disabled: true,
          required: false,
        },
      ];
      this.modalData = chapter;
      this.modalReadOnly = true;
      this.modalAction = "view-chapter";
      this.showModal = true;
    },
    editChapter(chapter, subjectId) {
      this.currentSubjectId = subjectId;
      this.modalTitle = "Edit Chapter";
      this.modalFields = [
        { name: "id", label: "ID", type: "number", disabled: true },
        { name: "name", label: "Name", type: "text" },
        {
          name: "description",
          label: "Description",
          type: "textarea",
          required: false,
        },
      ];
      this.modalData = chapter;
      this.modalReadOnly = false;
      this.modalAction = "edit-chapter";
      this.showModal = true;
    },
    async deleteChapter(chapterId) {
      this.openConfirmModal(
        "Are you sure you want to delete this chapter?",
        async () => {
          const toast = useToast();
          try {
            await axios.delete(`/admin/chapters/${chapterId}`);
            toast.success("Chapter deleted successfully.");
            this.fetchSubjects();
          } catch (e) {
            console.error("Failed to delete chapter:", e);
            toast.error("Failed to delete chapter.");
          }
        }
      );
    },
  },
};
</script>

<style scoped>
.page-layout {
  display: flex;
  min-height: 100vh;
  background-color: #f5f8fc;
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
  color: #26364a;
}

.subject-table {
  background-color: #ffffff;
  border: 1px solid #e3eaf1;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(100, 120, 140, 0.06);
  table-layout: fixed;
  overflow: hidden;
}

.subject-table th {
  background-color: #d1e8ff;
  color: #4e4e4e;
  text-align: center;
  font-weight: 600;

  border-color: #e1e9ee;
  padding: 11px;
}

.subject-table tbody tr:nth-child(odd) td {
  background-color: #ffffff;
}

.subject-table tbody tr:nth-child(even) td {
  background-color: #f9fafa;
}

.subject-table td {
  text-align: center;
  padding: 10px;

  color: #687585;
  background-color: #ffffff;

  border-color: #edf0f3;
}

.subject-table tbody tr:hover td {
  background-color: #f4f4f4 !important;
  transition: background-color 0.2s ease;
}

.subject-table .btn {
  font-size: 14px;
  margin: 5px;
}

.no-chapters-msg {
  padding: 15px 0;
  font-size: 0.95rem;
  color: #8a98a8 !important;
  background-color: #fafbfd;
  border: 1px dashed #d5dfe8;
  margin-top: 10px;
  border-radius: 5px;
}

.card {
  color: #526b7a;
  border: 1px solid #e3eaf1;
  box-shadow: 0 4px 10px rgba(100, 120, 140, 0.07);
  border-radius: 12px;
  margin-bottom: 20px;
  overflow: hidden;
}

.card:hover {
  box-shadow: 0 7px 16px rgba(100, 120, 140, 0.1);
  transform: scale(1.02);
  transition: all 0.2s ease-in-out;
}

.card-header {
  background-color: #6bc2e7;
  color: white;
  text-align: center;
  font-size: 20px;
  border: none;
  border-top-left-radius: 12px;
  border-top-right-radius: 12px;
  padding: 14px 16px;
}

.card-header h5 {
  margin: 0;
  font-weight: 600;
  letter-spacing: 0.2px;
}

.card-body {
  padding: 20px;
  background-color: #ffffff;
}

.card-footer {
  text-align: center;
  background-color: #f7f9fb;
  border-top: 1px solid #e5ebf0;
}

.btn-success {
  background-color: #56b875;
  color: white;
  border: none;
  padding: 7px;
}

.btn-success:hover {
  background-color: #3d9c5b;
}

.btn-warning {
  background-color: #ffbb00;
  border: none;
  color: white;
}

.btn-warning:hover {
  background-color: #faa11a;
  color: white;
}

.btn-danger {
  background-color: #f04848;
  border: none;
  color: white;
}

.btn-primary {
  background-color: #d19cdc;
  color: #ffffff;
  border: none;
}

.btn-primary:hover {
  background-color: #be86c9;
}

.btn-special {
  background-color: transparent;
  color: #278f91;
  border: 1.5px solid #278f91;
  padding: 0.7rem 1.4rem;
  font-size: 1.05rem;
  font-weight: 600;
  border-radius: 0.6rem;
  transition: all 0.2s ease-in-out;
}

.btn-special:hover {
  background-color: #2b9d9f;
  color: #ffffff;
  border-color: #278f91;
  transform: translateY(-1px);
}

.mt-3 .btn {
  margin: 0.5rem;
  padding: 0.6rem 0.9rem;
  border-radius: 5px;
}

@media (max-width: 768px) {
  .subject-table {
    font-size: 12px;
  }

  .subject-table th,
  .subject-table td {
    padding: 8px;
  }

  .subject-table .btn {
    font-size: 10px;
    padding: 4px 8px;
  }

  .card-body {
    overflow-x: auto;
  }
}
</style>
