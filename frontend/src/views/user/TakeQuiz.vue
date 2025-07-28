<template>
  <div class="take-quiz container mt-4">
    <h2 class="mb-3 text-center">Quiz Instructions</h2>

    <BaseLoader v-if="loading" />

    <BaseMessage v-else-if="error" :type="'error'" :message="error" />

    <div v-else>
      <div
        v-if="status === 'upcoming' || status === 'expired'"
        class="text-center"
      >
        <BaseMessage :type="'warning'" :message="message" />
        <button class="btn btn-outline-secondary mt-3" @click="goBack">
          Go Back
        </button>
      </div>

      <div v-if="status === 'available'" class="card shadow-sm p-4">
        <h4 class="mb-2 text-primary">{{ quizDetails.quiz_name }}</h4>

        <div class="quiz-details mb-3">
          <p><strong>Total Marks:</strong> {{ quizDetails.total_marks }}</p>
          <p><strong>Time Duration:</strong> {{ quizDetails.time_duration }}</p>
          <p v-if="quizDetails.remarks">
            <strong>Remarks:</strong> {{ quizDetails.remarks }}
          </p>
        </div>

        <div class="instructions mb-3">
          <h5 class="text-secondary">Instructions:</h5>
          <ol class="ps-3">
            <li v-for="(instruction, index) in instructions" :key="index">
              {{ instruction }}
            </li>
          </ol>

          <div class="mt-4">
            <h6 class="text-secondary mb-2">Question Status Legend:</h6>
            <div class="d-flex flex-wrap gap-3">
              <div class="d-flex align-items-center">
                <button class="btn btn-success btn-sm me-2" disabled>1</button>
                <span>Answered</span>
              </div>
              <div class="d-flex align-items-center">
                <button class="btn btn-primary btn-sm me-2" disabled>2</button>
                <span>Current Question</span>
              </div>
              <div class="d-flex align-items-center">
                <button class="btn btn-outline-primary btn-sm me-2" disabled>
                  3
                </button>
                <span>Unanswered</span>
              </div>
            </div>
          </div>
        </div>

        <div class="form-check mb-3">
          <input
            class="form-check-input"
            type="checkbox"
            id="agreeCheckbox"
            v-model="agreed"
          />
          <label class="form-check-label" for="agreeCheckbox">
            I have read and understood all instructions.
          </label>
        </div>

        <div v-if="agreed" class="text-center mb-3">
          <strong
            style="
              font-size: 1.4rem;
              font-family: 'Poppins', sans-serif;
              color: #2c3e50;
            "
            >All The Best!!</strong
          >
        </div>

        <button class="btn btn-primary" :disabled="!agreed" @click="startQuiz">
          Start Quiz
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import BaseLoader from "@/components/BaseLoader.vue";
import BaseMessage from "@/components/BaseMessage.vue";

export default {
  name: "TakeQuiz",
  components: {
    BaseLoader,
    BaseMessage,
  },
  data() {
    return {
      quizId: this.$route.params.quizId,
      status: "",
      quizDetails: {},
      instructions: [],
      message: "",
      error: null,
      loading: true,
      agreed: false,
    };
  },
  methods: {
    async fetchAvailability() {
      try {
        const res = await axios.get(
          `/user/take_quiz/${this.quizId}/availability`
        );
        this.status = res.data.status;

        if (this.status === "available") {
          this.instructions = res.data.general_instructions;
          this.quizDetails = res.data.quiz_details;
        } else {
          this.message = res.data.message;
        }
      } catch (err) {
        this.error =
          err.response?.data?.message || "Error checking quiz availability.";
      } finally {
        this.loading = false;
      }
    },
    startQuiz() {
      const key = `quiz-${this.quizId}`;

      localStorage.removeItem(`${key}-answers`);
      localStorage.removeItem(`${key}-timeLeft`);
      localStorage.removeItem(`${key}-submitted`);

      this.$router.push({ name: "StartQuiz", params: { quizId: this.quizId } });
    },
    goBack() {
      this.$router.push({ name: "QuizPage" });
    },
  },
  mounted() {
    this.fetchAvailability();
  },
};
</script>

<style scoped>
.take-quiz {
  max-width: 700px;
}

.card {
  border: 1px solid #dee2e6;
  border-radius: 8px;
  background-color: #fafafa;
}

.instructions ol {
  padding-left: 1.5rem;
}

.form-check-label {
  cursor: pointer;
}
</style>
