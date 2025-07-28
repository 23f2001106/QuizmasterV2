<template>
  <section
    id="home"
    class="home-container d-flex justify-content-center align-items-center text-center text-white"
    :style="{ backgroundImage: 'url(/bg.jpg)' }"
  >
    <div class="row justify-content-center align-items-center home-content">
      <div class="col text-center">
        <h1 class="display-4">Welcome to QuizMaster!</h1>
        <p>Your ultimate destination for quizzes</p>
        <div class="mt-4">
          <router-link to="/login" class="btn btn-dark btn-lg mx-3"
            >Login</router-link
          >
          <router-link to="/register" class="btn btn-light btn-lg mx-3"
            >Register</router-link
          >
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: "HomeSection",
};
</script>

<style scoped>
.home-container {
  height: 100vh;
  color: white;
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  display: flex;
  justify-content: center;
  align-items: center;
}

.home-content {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}

h1.display-4 {
  font-size: 5rem;
  font-family: Cambria, Cochin, Georgia, Times, "Times New Roman", serif;
  font-weight: bold;
}

#home p {
  font-size: 2rem;
  margin-bottom: 20px;
  font-family: Cambria, Cochin, Georgia, Times, "Times New Roman", serif;
  font-weight: 500;
}

.btn-light {
  background-color: #d1ab7f;
  color: #fff;
  border: 1px solid transparent;
  font-size: 1.5rem;
  padding: 11px 25px;
}

.btn-dark {
  background-color: #503118;
  color: #fff;
  border: 1px solid transparent;
  font-size: 1.5rem;
  padding: 11px 25px;
}

.btn:hover {
  background-color: transparent;
  color: #fff;
  border: 1px solid #fff;
  transition: all 0.3s ease;
}
</style>
