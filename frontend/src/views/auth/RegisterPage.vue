<template>
  <div class="register-wrapper d-flex flex-column min-vh-100">
    <NavBar />

    <div
      class="flex-grow-1 d-flex justify-content-center align-items-center register-page"
      :style="{ backgroundImage: 'url(/bg2.jpg)' }"
    >
      <div v-if="!showOtpVerification" class="register-card p-4 rounded">
        <h2 class="mb-4 text-center">Create Account</h2>

        <form @submit.prevent="handleRegister">
          <div class="mb-3">
            <label for="email" class="form-label"
              >Username <span class="text-danger">*</span></label
            >
            <input
              v-model="form.email"
              type="email"
              id="email"
              class="form-control"
              placeholder="Email"
              required
            />
          </div>

          <div class="mb-3">
            <label for="name" class="form-label"
              >Full Name <span class="text-danger">*</span></label
            >
            <input
              v-model="form.name"
              type="text"
              id="name"
              class="form-control"
              placeholder="Full Name"
              required
            />
          </div>

          <div class="mb-3">
            <label for="qualification" class="form-label">Qualification</label>
            <input
              v-model="form.qualification"
              type="text"
              id="qualification"
              class="form-control"
              placeholder="Qualification"
            />
          </div>

          <div class="mb-3">
            <label for="dob" class="form-label">Date of Birth</label>
            <input
              v-model="form.dob"
              type="date"
              id="dob"
              class="form-control"
            />
          </div>

          <div class="mb-3">
            <label for="password" class="form-label"
              >Password <span class="text-danger">*</span></label
            >
            <input
              v-model="form.password"
              type="password"
              id="password"
              class="form-control"
              placeholder="Password"
              required
            />
          </div>

          <div class="mb-3">
            <label for="confirmPassword" class="form-label"
              >Confirm Password <span class="text-danger">*</span></label
            >
            <input
              v-model="form.confirmPassword"
              type="password"
              id="confirmPassword"
              class="form-control"
              placeholder="Re-enter password"
              required
            />
            <div
              v-if="
                form.confirmPassword && form.confirmPassword !== form.password
              "
              class="text-danger small mt-1"
            >
              Passwords do not match.
            </div>
          </div>
          <BaseLoader v-if="loading" />
          <BaseMessage v-if="error" :message="error" type="error" />
          <BaseMessage v-if="success" :message="success" type="success" />

          <div class="text-center mt-3">
            <button
              type="submit"
              class="btn btn-lg signup-btn"
              :disabled="form.password !== form.confirmPassword || loading"
            >
              Sign Up
            </button>
          </div>
        </form>

        <p class="mt-4 text-center">
          Already have an account?
          <router-link to="/login" class="text-decoration-none"
            >Login</router-link
          >
        </p>
      </div>
      <OtpVerification
        v-if="showOtpVerification"
        :user-id="userIdForOtp"
        context="register"
        endpoint="/auth/verify-email"
        @verified="handleOtpVerified"
      />
    </div>

    <AppFooter />
  </div>
</template>

<script>
import axios from "axios";
import NavBar from "@/components/NavBar.vue";
import AppFooter from "@/components/AppFooter.vue";
import OtpVerification from "@/components/auth/OtpVerification.vue";
import BaseLoader from "@/components/BaseLoader.vue";
import BaseMessage from "@/components/BaseMessage.vue";

export default {
  name: "RegisterPage",
  components: {
    NavBar,
    AppFooter,
    OtpVerification,
    BaseLoader,
    BaseMessage,
  },
  data() {
    return {
      form: {
        email: "",
        name: "",
        qualification: "",
        dob: "",
        password: "",
        confirmPassword: "",
      },
      userIdForOtp: null,
      showOtpVerification: false,
      loading: false,
      error: null,
      success: null,
    };
  },
  methods: {
    async handleRegister() {
      const { email, name, password, confirmPassword, qualification, dob } =
        this.form;

      this.error = null;
      this.success = null;

      if (!email || !name || !password || !confirmPassword) {
        this.error = "Please fill all required fields.";
        return;
      }

      if (password !== confirmPassword) {
        this.error = "Passwords do not match.";
        return;
      }
      this.loading = true;
      try {
        const response = await axios.post("/auth/register", {
          username: email,
          password,
          full_name: name,
          qualification,
          dob,
        });

        this.userIdForOtp = response.data.user_id;
        this.success = "Registration successful. Please verify your email.";
        this.showOtpVerification = true;
      } catch (error) {
        this.error = error.response?.data?.message || "Registration failed.";
      } finally {
        this.loading = false;
      }
    },
    handleOtpVerified() {
      alert("Account verified successfully!");
      this.$router.push("/login");
    },
  },
};
</script>

<style scoped>
.register-wrapper {
  min-height: 100vh;
}

.register-page {
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

.register-card {
  background-color: #f9f9f9;
  max-width: 550px;
  width: 100%;
  border: 1px solid #ddd;
  margin-top: 80px;
  margin-bottom: 50px;
}

.signup-btn {
  display: block;
  background-color: #d1ab7f;
  border: 1px solid transparent;
  color: rgb(255, 255, 255);
  margin: 0 auto;
  min-width: 140px;
}

.signup-btn:hover {
  background-color: transparent;
  border: 1px solid #5c4033;
  color: #5c4033;
  transition: all 0.3 ease;
}

input:focus,
button:focus {
  box-shadow: none;
  outline: none;
}
</style>
