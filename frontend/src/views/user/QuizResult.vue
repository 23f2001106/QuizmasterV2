<template>
  <div class="result-container my-5 px-3 px-md-5 d-flex justify-content-center">
    <BaseLoader v-if="loading" />
    <div v-else class="result-card p-4 shadow rounded text-center">
      <img src="@/assets/Trophy.png" alt="Trophy" class="trophy-img mb-3" />

      <h3 class="feedback-message mb-3">
        {{ result.message }}
      </h3>

      <h5 class="quiz-name text-uppercase mb-2">{{ result.quiz_name }}</h5>
      <p class="text-muted mb-3">Attempted on: {{ result.attempted_on }}</p>

      <div class="score-box mb-3">
        <h4 class="score-text">{{ result.score }}</h4>
        <p>Percentage: {{ result.percentage }}%</p>
        <p>Time Taken: {{ result.time_taken }}</p>
      </div>

      <router-link to="/user/dashboard" class="btn btn-primary mt-3">
        Go to Dashboard
      </router-link>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useToast } from "vue-toastification";
import BaseLoader from "@/components/BaseLoader.vue";

export default {
  name: "QuizResult",
  components: {
    BaseLoader,
  },
  data() {
    return {
      loading: true,
      result: {
        quiz_name: "",
        score: "",
        percentage: 0,
        time_taken: "",
        message: "",
        attempted_on: "",
      },
    };
  },
  async created() {
    const quizId = this.$route.params.quizId;
    const toast = useToast();

    try {
      const res = await axios.get(`/user/quiz_result/${quizId}`);
      this.result = res.data;
    } catch (err) {
      toast.error("Error showing results.");
      this.$router.push("/user/dashboard");
    } finally {
      this.loading = false;
    }
  },
};
</script>

<style scoped>
.result-container {
  max-width: 600px;
  margin: auto;
}

.result-card {
  background-color: #ffffff;
  border: 1px solid #e2e2e2;
}

.trophy-img {
  width: 100px;
  height: auto;
}

.feedback-message {
  font-size: 1.8rem;
  font-weight: bold;
  color: #333;
}

.quiz-name {
  font-weight: 600;
  color: #0dcaba;
}

.score-box {
  background-color: #f8f9fa;
  border-radius: 10px;
  padding: 15px;
}

.score-text {
  font-size: 2rem;
  color: #28a745;
  font-weight: 700;
}
</style>
