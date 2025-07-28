<template>
  <div class="quiz-container">
    <BaseLoader v-if="loading" />

    <!-- Quiz Header Banner -->
    <div v-else>
      <div class="quiz-header">
        <h2>{{ quizName }}</h2>
      </div>

      <!-- Timer Below Header -->
      <div class="d-flex justify-content-end mb-3 px-4 py-2">
        <div class="fw-bold fs-5 text-danger">
          Time Left: {{ formattedTime }}
        </div>
      </div>

      <!-- Main Quiz Layout -->
      <div class="d-flex flex-row">
        <div
          class="question-section card p-4 me-3 flex-grow-1 overflow-auto"
          v-if="currentQuestion"
        >
          <h5>Question {{ currentQuestion.serial_number }}:</h5>
          <p>{{ currentQuestion.question_statement }}</p>

          <div class="options">
            <div
              v-for="option in currentQuestion.options"
              :key="option.value"
              class="option-container"
              @click="selectOption(currentQuestion.id, option.value)"
            >
              <input
                class="form-check-input"
                type="radio"
                :name="'question-' + currentQuestion.id"
                :id="'q-' + currentQuestion.id + '-option-' + option.value"
                :value="option.value"
                v-model="selectedAnswers[currentQuestion.id]"
                :disabled="isSubmitted"
              />
              <label
                class="form-check-label"
                :for="'q-' + currentQuestion.id + '-option-' + option.value"
              >
                {{ option.text }}
              </label>
            </div>
          </div>

          <button
            class="btn btn-warning btn-sm clear-btn"
            @click="clearAnswer(currentQuestion.id)"
          >
            Clear
          </button>
        </div>

        <div class="question-nav-panel d-flex flex-column align-items-center">
          <div class="panel-box card shadow-sm p-3 w-100 d-flex flex-column">
            <div class="question-nav-grid overflow-auto flex-grow-1 mb-3">
              <button
                v-for="(q, index) in questions"
                :key="q.id"
                class="btn btn-sm nav-btn my-1"
                :class="buttonClass(q, index)"
                @click="goToQuestion(index)"
              >
                {{ q.serial_number }}
              </button>
            </div>

            <!-- Action Buttons -->
            <div class="action-buttons d-flex flex-column align-items-center">
              <button
                class="btn btn-secondary mb-2"
                @click="goToPrevious"
                :disabled="currentIndex === 0"
              >
                Previous
              </button>
              <button
                class="btn btn-primary mb-2"
                @click="goToNext"
                :disabled="currentIndex === questions.length - 1"
              >
                Next
              </button>
              <button
                class="btn btn-danger"
                @click="confirmSubmit"
                :disabled="isSubmitted"
              >
                Submit
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Confirm Modal -->
      <ConfirmModal
        v-if="showModal"
        title="Submit Quiz"
        message="Are you sure you want to submit the quiz?"
        @confirm="submitQuiz"
        @cancel="showModal = false"
      />
    </div>
  </div>
</template>

<script>
import ConfirmModal from "@/components/ConfirmModal.vue";
import BaseLoader from "@/components/BaseLoader.vue";
import axios from "axios";

export default {
  name: "StartQuiz",
  components: { ConfirmModal, BaseLoader },

  data() {
    return {
      quizId: this.$route.params.quizId,
      quizName: "",
      questions: [],
      currentIndex: 0,
      selectedAnswers: {},
      timeLeft: 0,
      timeDuration: 0,
      timer: null,
      showModal: false,
      isSubmitted: false,
      loading: true,
    };
  },

  computed: {
    currentQuestion() {
      return this.questions[this.currentIndex] || null;
    },
    formattedTime() {
      const m = Math.floor(this.timeLeft / 60);
      const s = this.timeLeft % 60;
      return `${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
    },
  },

  created() {
    this.fetchQuiz();
    window.addEventListener("beforeunload", this.preventUnload);
  },

  beforeUnmount() {
    clearInterval(this.timer);
    window.removeEventListener("beforeunload", this.preventUnload);
  },

  methods: {
    async fetchQuiz() {
      try {
        const res = await axios.get(`/user/start_quiz/${this.quizId}`);
        this.quizName = res.data.quiz_name;
        this.questions = res.data.questions;

        this.timeDuration = this.parseDuration(res.data.time_duration);
        this.restoreAnswers();
        this.timeLeft = this.restoreTime() || this.timeDuration;

        console.log("Time Duration string:", res.data.time_duration);
        console.log("Parsed Duration seconds:", this.timeDuration);
        console.log("Is Submitted:", this.isSubmitted);
        if (!this.isSubmitted) {
          this.startTimer();
        }
      } catch (err) {
        alert("Failed to load quiz: " + err.response?.data?.message);
      } finally {
        this.loading = false;
      }
    },

    parseDuration(str) {
      const [h, m, s] = str.split(":").map(Number);
      return h * 3600 + m * 60 + s;
    },

    restoreTime() {
      return (
        parseInt(localStorage.getItem(`quiz-${this.quizId}-timeLeft`)) || 0
      );
    },

    restoreAnswers() {
      const saved = localStorage.getItem(`quiz-${this.quizId}-answers`);
      const submitted = localStorage.getItem(`quiz-${this.quizId}-submitted`);
      this.isSubmitted = submitted === "true";

      if (saved) this.selectedAnswers = JSON.parse(saved);
    },

    startTimer() {
      this.timer = setInterval(() => {
        if (this.timeLeft > 0) {
          this.timeLeft--;
          localStorage.setItem(`quiz-${this.quizId}-timeLeft`, this.timeLeft);
        } else {
          clearInterval(this.timer);
          this.submitQuiz();
        }
      }, 1000);
    },

    preventUnload(event) {
      if (!this.isSubmitted) {
        event.preventDefault();
        event.returnValue = "";
      }
    },

    selectOption(qid, val) {
      if (this.isSubmitted) return;
      this.selectedAnswers[qid] = val;
      localStorage.setItem(
        `quiz-${this.quizId}-answers`,
        JSON.stringify(this.selectedAnswers)
      );
    },

    clearAnswer(qid) {
      if (this.isSubmitted) return;
      delete this.selectedAnswers[qid];
      localStorage.setItem(
        `quiz-${this.quizId}-answers`,
        JSON.stringify(this.selectedAnswers)
      );
    },

    buttonClass(question, index) {
      if (this.currentIndex === index) {
        return "btn-primary";
      } else if (this.selectedAnswers[question.id] !== undefined) {
        return "btn-success";
      } else {
        return "btn-outline-primary";
      }
    },

    goToQuestion(i) {
      if (!this.isSubmitted) this.currentIndex = i;
    },

    goToPrevious() {
      if (this.currentIndex > 0 && !this.isSubmitted) this.currentIndex--;
    },

    goToNext() {
      if (this.currentIndex < this.questions.length - 1 && !this.isSubmitted)
        this.currentIndex++;
    },

    confirmSubmit() {
      this.showModal = true;
    },

    async submitQuiz() {
      this.showModal = false;
      clearInterval(this.timer);

      const payload = {
        answers: Object.entries(this.selectedAnswers).map(
          ([qid, selected]) => ({
            question_id: parseInt(qid),
            selected_option: selected,
          })
        ),
        time_taken: this.timeDuration - this.timeLeft,
      };

      try {
        await axios.post(`/user/submit_quiz/${this.quizId}`, payload);
        const key = `quiz-${this.quizId}`;
        localStorage.removeItem(`${key}-answers`);
        localStorage.removeItem(`${key}-timeLeft`);
        localStorage.removeItem(`${key}-submitted`);
        this.isSubmitted = true;

        this.$router.push({
          name: "QuizResult",
          params: { quizId: this.quizId },
        });
      } catch (err) {
        alert("Error submitting quiz.");
      }
    },
  },
};
</script>

<style scoped>
.quiz-header {
  padding: 20px;
  text-align: left;
  background-color: #0dcaba;
  color: white;
  width: 100%;
  margin-bottom: 10px;
}

.quiz-header h2 {
  margin: 0;
  font-size: 2.5rem;
}

.question-section {
  height: 80vh;
  width: 100%;
  margin: 1rem;
  overflow-y: auto;
}

.question-nav-panel {
  width: 400px;
  height: 80vh;
  margin: 1rem;
}

.panel-box {
  height: 100%;
  background-color: #ffffff;
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.question-nav-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-gap: 8px;
  padding-right: 4px;
  overflow-y: auto;
  flex-grow: 1;
}

.nav-btn {
  font-weight: bold;
  border-radius: 8px;
  width: 50px;
  height: 50px;
  padding: 0;
  text-align: center;
  line-height: 50px;
}

.options {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.options .option-container {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 12px 15px;
  display: flex;
  align-items: center;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.options .option-container:hover {
  background-color: #ececec;
}

.options input[type="radio"] {
  margin-right: 10px;
}

.clear-btn {
  width: fit-content;
  padding: 6px 16px;
  font-size: 0.9rem;
  margin-top: 20px;
  border: 1px solid #000;
  color: #000;
  background-color: transparent;
  transition: all 0.3s ease;
}

.clear-btn:hover {
  background-color: #555;
  color: #fff;
  border-color: #555;
}
</style>
