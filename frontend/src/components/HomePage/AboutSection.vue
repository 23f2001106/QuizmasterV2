<template>
  <section id="about" class="about-container">
    <div class="about-content">
      <h2 class="about-title">ABOUT US</h2>
      <p class="about-text">
        Quizmaster is your all-in-one exam preparation platform designed to make
        studying efficient, engaging, and stress-free. With intuitive tools and
        smart features, Quizmaster helps learners stay on track and succeed in
        their academic goals.
      </p>
    </div>
  </section>
</template>

<script>
export default {
  name: "AboutSection",
};
</script>

<style scoped>
.about-container {
  text-align: center;
  padding: 60px 20px;
  background-color: #f9f9f9;
}

.about-title {
  font-weight: bold;
  text-transform: uppercase;
  position: relative;
  display: inline-block;
  color: #333;
  margin-bottom: 20px;
}

.about-title:hover {
  transform: scale(1.05);
  transition: all 0.3s ease;
}

.about-title::after {
  content: " ";
  display: block;
  width: 60px;
  height: 2px;
  background-color: #a97449;
  margin: 8px auto 0;
}

.about-text {
  max-width: 700px;
  margin: 0 auto;
  text-align: justify;
  font-size: 1.1rem;
  color: #555;
  line-height: 1.6;
}
</style>
