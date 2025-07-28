<template>
  <section id="features" class="features-section d-flex">
    <!-- Left Side: Image and Description -->
    <div
      class="features-left d-flex align-items-center justify-content-center"
      :style="{ backgroundImage: 'url(/feature-bg.jpg)' }"
    >
      <div
        class="feature-description text-white text-center"
        v-if="activeFeatureIndex !== null"
      >
        <h3>{{ activeFeature.title }}</h3>
        <p>{{ activeFeature.description }}</p>
      </div>
    </div>

    <!-- Right Side: Feature Titles -->
    <div class="features-right d-flex flex-column justify-content-center">
      <div class="features-heading text-white mb-4 text-center">
        <h2 class="features-title">Explore Our Key Features</h2>
      </div>
      <div
        v-for="(feature, index) in features"
        :key="index"
        class="feature-title-card"
        @mouseover="setActiveFeature(index)"
        @mouseleave="clearActiveFeature"
      >
        <h5>{{ feature.title }}</h5>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: "FeaturesSection",
  data() {
    return {
      // Features Section Data
      features: [
        {
          title: "Take Timed Quizzes",
          description:
            "Test your knowledge with subject-based quizzes under real exam conditions to improve time management and accuracy.",
        },
        {
          title: "Track Your Progress",
          description:
            "Monitor your scores and performance trends to stay motivated and focused on areas that need improvement.",
        },
        {
          title: "Review Answers",
          description:
            "Go over correct answers after quizzes to learn from your mistakes and strengthen your understanding.",
        },
        {
          title: "Search & Explore",
          description:
            "Quickly discover quizzes by topic, course, or difficulty level using our smart filtering tools.",
        },
        {
          title: "Personalized Experience",
          description:
            "Customize your study experience and keep track of your quiz history, preferences, and goals.",
        },
      ],
      activeFeatureIndex: null,
    };
  },
  computed: {
    activeFeature() {
      return this.features[this.activeFeatureIndex];
    },
  },
  methods: {
    // Features section hover methods
    setActiveFeature(index) {
      this.activeFeatureIndex = index;
    },
    clearActiveFeature() {
      this.activeFeatureIndex = null;
    },
  },
};
</script>

<style scoped>
.features-section {
  height: 100vh;
  display: flex;
  flex-direction: row;
}

.features-left {
  flex: 1;
  background-size: cover;
  background-position: center;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
}

.features-left::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1;
}

.features-title {
  font-size: 1.6rem;
  font-weight: bold;
  text-transform: uppercase;
  position: relative;
  color: #fff;
  display: inline-block;
  margin-bottom: 10px;
}

.features-title::after {
  content: "";
  display: block;
  width: 60px;
  height: 2px;
  background-color: #f5e1a4;
  margin: 6px auto 0;
}

.features-title:hover {
  transform: scale(1.05);
  transition: all 0.3s ease;
}

.feature-description {
  z-index: 2;
  max-width: 500px;
  padding: 30px;
  color: white;
}

.feature-description h3 {
  font-weight: bold;
  font-size: 1.8rem;
  margin-bottom: 15px;
  text-transform: uppercase;
  border-bottom: 2px solid #a97449;
  display: inline-block;
  padding-bottom: 5px;
}

.feature-description p {
  font-size: 1.1rem;
  line-height: 1.6;
}

.features-right {
  flex: 1;
  background-color: #5c4033;
  padding: 40px 30px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 20px;
}

.feature-title-card {
  background-color: #fff;
  color: #333;
  padding: 15px 20px;
  margin: 8px auto;
  width: 80%;
  max-width: 300px;
  border-radius: 30px;
  cursor: pointer;
  text-align: center;
  transition: all 0.3s ease;
  font-weight: bold;
  text-transform: uppercase;
  border: 1px solid transparent;
}

.feature-title-card:hover {
  background-color: transparent;
  color: #fff;
  border: 1px solid #fff;
}
</style>
