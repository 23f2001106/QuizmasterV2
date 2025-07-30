<template>
  <div class="page-layout">
    <SideBar />

    <div class="main-content">
      <BaseLoader v-if="loading" />

      <div v-else>
        <header class="page-header">
          <h2>Welcome, Admin</h2>
        </header>

        <h4 class="section-title p-4">Quizzes</h4>
        <div class="text-center mt-4 mb-4">
          <button class="btn btn-special" @click="openQuizModal('add')">
            Add Quiz
          </button>
        </div>
        <div class="row">
          <template v-if="quizzes.length">
            <div v-for="quiz in quizzes" :key="quiz.id" class="col-md-6 mb-3">
              <div class="card">
                <div class="card-header">
                  <h5>{{ quiz.name }}</h5>
                </div>

                <div class="card-body">
                  <table class="table table-striped table-bordered quiz-table">
                    <thead>
                      <tr>
                        <th>ID</th>
                        <th>Question</th>
                        <th>Action</th>
                      </tr>
                    </thead>
                    <tbody>
                      <template v-if="quiz.questions.length">
                        <tr v-for="q in quiz.questions" :key="q.id">
                          <td>{{ q.id }}</td>
                          <td>{{ q.question_statement }}</td>
                          <td>
                            <button
                              class="btn btn-primary btn-sm"
                              @click="viewQuestion(q, quiz.id)"
                            >
                              View
                            </button>
                            <button
                              class="btn btn-warning btn-sm"
                              @click="editQuestion(q, quiz.id)"
                            >
                              Edit
                            </button>
                            <button
                              class="btn btn-danger btn-sm"
                              @click="deleteQuestion(q.id)"
                            >
                              Delete
                            </button>
                          </td>
                        </tr>
                      </template>
                      <tr v-else>
                        <td colspan="3" class="text-center text-muted">
                          No questions added
                        </td>
                      </tr>
                    </tbody>
                  </table>

                  <button
                    class="btn btn-success btn-sm"
                    @click="addQuestion(quiz.id)"
                  >
                    Add Question
                  </button>

                  <div class="mt-3 text-center">
                    <button
                      class="btn btn-primary btn-sm"
                      @click="openQuizModal('view', quiz)"
                    >
                      View Quiz
                    </button>
                    <button
                      class="btn btn-warning btn-sm"
                      @click="openQuizModal('edit', quiz)"
                    >
                      Edit Quiz
                    </button>
                    <button
                      class="btn btn-danger btn-sm"
                      @click="deleteQuiz(quiz.id)"
                    >
                      Delete Quiz
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </template>

          <p v-else class="text-center text-muted w-100 p-4">
            No quizzes found. Click "Add Quiz" to create one.
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
    @close="handleModalClose"
    @form-submit="handleFormSubmit"
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
  name: "QuizPage",
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
      quizzes: [],
      chapters: [],
      showModal: false,
      modalTitle: "",
      modalFields: [],
      modalData: {},
      modalReadOnly: false,
      modalAction: "",
      quizIdForQuestion: null,
      confirmModal: {
        show: false,
        title: "Please Confirm",
        message: "",
        onConfirm: null,
      },
    };
  },
  mounted() {
    this.fetchQuizzes();
    this.fetchChapters();
  },
  methods: {
    async fetchChapters() {
      try {
        const res = await axios.get("/admin/chapters/all");
        this.chapters = res.data;
      } catch (e) {
        console.error("Failed to load chapters:", e);
      }
    },

    async fetchQuizzes() {
      this.loading = true;
      try {
        const res = await axios.get("/admin/quiz");
        this.quizzes = res.data;
      } catch (e) {
        console.error("Failed to fetch quizzes:", e);
      } finally {
        this.loading = false;
      }
    },
    formatDate(date) {
      return new Date(date).toLocaleString();
    },
    handleModalClose() {
      this.showModal = false;
      this.quizIdForQuestion = null;
    },
    addQuiz() {
      this.modalTitle = "Add Quiz";
      this.modalFields = [
        {
          name: "chapter_id",
          label: "Chapter",
          type: "select",
          options: this.chapters.map((c) => ({
            value: c.id,
            label: `${c.id} - ${c.name}`,
          })),
        },
        { name: "name", label: "Quiz Name", type: "text" },
        { name: "date_of_quiz", label: "Start Date", type: "date" },
        { name: "due_date", label: "Due Date", type: "date" },
        {
          name: "time_duration",
          label: "Duration (HH:MM:SS)",
          type: "duration",
        },
        {
          name: "remarks",
          label: "Remarks",
          type: "textarea",
          required: false,
        },
      ];
      this.modalData = {};
      this.modalReadOnly = false;
      this.modalAction = "add";
      this.showModal = true;
    },

    async viewQuiz(quiz) {
      try {
        const res = await axios.get(`/admin/quizzes/${quiz.id}`);
        const fullQuiz = res.data;

        // Flatten the data so nested objects become simple strings
        const quizForModal = {
          id: fullQuiz.id,
          name: fullQuiz.name,
          chapter: fullQuiz.chapter.name,
          subject: fullQuiz.subject.name,
          date_of_quiz: this.formatDate(fullQuiz.date_of_quiz),
          due_date: this.formatDate(fullQuiz.due_date),
          time_duration: fullQuiz.time_duration,
          remarks: fullQuiz.remarks,
          question_count: fullQuiz.question_count,
          date_created: this.formatDate(fullQuiz.date_created),
        };

        this.modalFields = [
          { name: "id", label: "ID", type: "number", disabled: true },
          { name: "name", label: "Name", type: "text", disabled: true },
          { name: "chapter", label: "Chapter", type: "text", disabled: true },
          { name: "subject", label: "Subject", type: "text", disabled: true },
          {
            name: "date_of_quiz",
            label: "Start Date",
            type: "text",
            disabled: true,
          },
          { name: "due_date", label: "Due Date", type: "text", disabled: true },
          {
            name: "time_duration",
            label: "Duration",
            type: "duration",
            disabled: true,
          },
          {
            name: "remarks",
            label: "Remarks",
            type: "textarea",
            disabled: true,
          },
          {
            name: "question_count",
            label: "Number of Questions",
            type: "number",
            disabled: true,
          },
          {
            name: "date_created",
            label: "Created At",
            type: "text",
            disabled: true,
          },
        ];

        this.modalData = quizForModal;
        this.modalReadOnly = true;
        this.modalAction = "view";
        this.showModal = true;
      } catch (e) {
        console.error("Failed to load quiz details:", e);
      }
    },
    editQuiz(quiz) {
      this.modalTitle = "Edit Quiz";
      this.modalFields = [
        { name: "id", label: "ID", type: "number", disabled: true },
        { name: "name", label: "Quiz Name", type: "text" },
        { name: "date_of_quiz", label: "Start Date", type: "date" },
        { name: "due_date", label: "Due Date", type: "date" },
        { name: "time_duration", label: "Duration", type: "duration" },
        {
          name: "remarks",
          label: "Remarks",
          type: "textarea",
          required: false,
        },
      ];
      this.modalData = {
        ...quiz,
        date_of_quiz: quiz.date_of_quiz
          ? quiz.date_of_quiz.substring(0, 10)
          : "",
        due_date: quiz.due_date ? quiz.due_date.substring(0, 10) : "",
      };
      this.modalReadOnly = false;
      this.modalAction = "edit";
      this.showModal = true;
    },
    openQuizModal(mode, quiz = {}) {
      if (mode === "add") return this.addQuiz();
      if (mode === "view") return this.viewQuiz(quiz);
      if (mode === "edit") return this.editQuiz(quiz);
    },

    addQuestion(quizId) {
      this.quizIdForQuestion = quizId;
      this.modalTitle = "Add Question";
      this.modalFields = this.questionFields();
      this.modalData = {};
      this.modalReadOnly = false;
      this.modalAction = "add-question";
      this.showModal = true;
    },
    async editQuestion(question, quizId) {
      this.quizIdForQuestion = quizId;
      try {
        const res = await axios.get(`/admin/questions/${question.id}`);
        const questionDetails = res.data;

        const questionCopy = {
          id: questionDetails.id,
          question_statement: questionDetails.question_statement,
          option1: questionDetails.option1 || "",
          option2: questionDetails.option2 || "",
          option3: questionDetails.option3 || "",
          option4: questionDetails.option4 || "",
          correct_option: questionDetails.correct_option || "",
        };

        this.modalTitle = "Edit Question";
        this.modalFields = this.questionFields();
        this.modalData = questionCopy;
        this.modalReadOnly = false;
        this.modalAction = "edit-question";
        this.showModal = true;
      } catch (error) {
        console.error("Failed to load question details:", error);
      }
    },

    async viewQuestion(question, quizId) {
      this.quizIdForQuestion = quizId;

      try {
        const res = await axios.get(`/admin/questions/${question.id}`);
        const questionDetails = res.data;
        console.log(questionDetails);
        const questionCopy = {
          id: questionDetails.id,
          question_statement: questionDetails.question_statement,
          option1: questionDetails.option1 || "",
          option2: questionDetails.option2 || "",
          option3: questionDetails.option3 || "",
          option4: questionDetails.option4 || "",
          correct_option: questionDetails.correct_option || "",
        };

        this.modalTitle = "View Question";
        this.modalFields = this.questionFields(true);
        this.modalData = questionCopy;
        this.modalReadOnly = true;
        this.modalAction = "view-question";
        this.showModal = true;
      } catch (e) {
        console.error("Failed to load question details:", e);
      }
    },
    questionFields(readOnly = false) {
      return [
        {
          name: "question_statement",
          label: "Question",
          type: "textarea",
          disabled: readOnly,
        },
        {
          name: "option1",
          label: "Option 1",
          type: "text",
          disabled: readOnly,
        },
        {
          name: "option2",
          label: "Option 2",
          type: "text",
          disabled: readOnly,
        },
        {
          name: "option3",
          label: "Option 3",
          type: "text",
          disabled: readOnly,
        },
        {
          name: "option4",
          label: "Option 4",
          type: "text",
          disabled: readOnly,
        },
        {
          name: "correct_option",
          label: "Correct Option",
          type: "select",
          options: [
            { value: 1, label: "1" },
            { value: 2, label: "2" },
            { value: 3, label: "3" },
            { value: 4, label: "4" },
          ],
          disabled: readOnly,
        },
      ];
    },
    async handleFormSubmit(data) {
      const toast = useToast();
      try {
        if (this.modalAction === "add") {
          await axios.post("/admin/quiz", data);
          toast.success("Quiz added");
        } else if (this.modalAction === "edit") {
          await axios.put(`/admin/quizzes/${data.id}`, data);
          toast.success("Quiz updated");
        } else if (this.modalAction === "add-question") {
          await axios.post(
            `/admin/quizzes/${this.quizIdForQuestion}/questions`,
            data
          );
          toast.success("Question added");
        } else if (this.modalAction === "edit-question") {
          await axios.put(`/admin/questions/${data.id}`, data);
          toast.success("Question updated");
        }
        this.fetchQuizzes();
      } catch (e) {
        toast.error("Form submission failed");
        console.error(e);
      } finally {
        this.showModal = false;
      }
    },
    deleteQuiz(id) {
      this.openConfirmModal(
        "Are you sure you want to delete this quiz?",
        async () => {
          const toast = useToast();
          try {
            await axios.delete(`/admin/quizzes/${id}`);
            toast.success("Quiz deleted");
            this.fetchQuizzes();
          } catch (e) {
            toast.error("Failed to delete quiz");
          }
        }
      );
    },
    deleteQuestion(id) {
      this.openConfirmModal(
        "Are you sure you want to delete this question?",
        async () => {
          const toast = useToast();
          try {
            await axios.delete(`/admin/questions/${id}`);
            toast.success("Question deleted");
            this.fetchQuizzes();
          } catch (e) {
            toast.error("Failed to delete question");
          }
        }
      );
    },
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
      this.confirmModal = {
        show: false,
        title: "Please Confirm",
        message: "",
        onConfirm: null,
      };
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
.quiz-table {
  background-color: #ffffff;
  border: 1px solid #dfe3e8;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  table-layout: fixed;
}

.quiz-table th {
  background-color: #4caf50;
  color: #ffffff;
  text-align: center;
}

.quiz-table td {
  text-align: center;
  padding: 10px;
}

.quiz-table tbody tr:hover td {
  background-color: #f7f9fc !important;
  transition: background-color 0.2s ease;
}

.quiz-table .btn {
  margin: 0 5px;
  font-size: 14px;
  margin: 5px;
}

@media (max-width: 768px) {
  .quiz-table {
    font-size: 12px;
  }

  .quiz-table th,
  .quiz-table td {
    padding: 8px;
  }

  .quiz-table .btn {
    font-size: 10px;
    padding: 4px 8px;
  }

  .card-body {
    overflow-x: auto;
  }
}

.card {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  margin-bottom: 20px;
}

.card:hover {
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.12);
  transform: scale(1.02);
  transition: all 0.2s ease-in-out;
}

.card-header {
  background-color: #61d67f;
  color: white;
  text-align: center;
  font-size: 20px;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
}

.card-body {
  padding: 20px;
}

.card-footer {
  text-align: center;
  background-color: #f8f9fa;
}

.btn-success {
  background-color: #56b875;
  color: white;
  border-radius: 5px;
}

.btn-success:hover {
  background-color: #3d9c5b;
}

.btn-warning {
  background-color: #ff9800;
  border: none;
  color: white;
}

.btn-warning:hover {
  background-color: #e88f09;
  border: none;
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
  background-color: #b176bb;
  color: #ffffff;
}

.btn-special {
  background-color: rgb(32, 192, 187);
  color: #ffffff;
  padding: 1rem;
  font-size: 1.25rem;
  font-weight: 400;
  border-radius: 0.6rem;
}

.btn-special:hover {
  background-color: transparent;
  color: rgb(32, 192, 187);
  border: 1px solid rgb(32, 192, 187);
}

.mt-3 .btn {
  margin: 0.5rem;
  padding: 0.6rem;
}
</style>
