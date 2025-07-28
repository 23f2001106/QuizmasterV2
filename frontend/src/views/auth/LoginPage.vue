<template>
  <div class="login-wrapper d-flex flex-column min-vh-100">
    <NavBar />

    <div
      class="login-page flex-grow-1 d-flex justify-content-center align-items-center"
      :style="{ backgroundImage: 'url(/coffee-bg.jpg)' }"
    >
      <div class="login-card p-4 rounded">
        <h2 class="mb-4 text-center">Login</h2>

        <form @submit.prevent="handleLogin">
          <div class="mb-3">
            <label for="username" class="form-label">Username</label>
            <input
              v-model="username"
              type="text"
              id="username"
              class="form-control"
              placeholder="Username"
              required
            />
          </div>

          <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input
              v-model="password"
              type="password"
              id="password"
              class="form-control"
              placeholder="Password"
              required
            />
            <div class="text-end mt-1">
              <router-link
                to="/reset-password"
                class="text-decoration-none small"
              >
                Forgot Password?
              </router-link>
            </div>
          </div>

          <BaseLoader v-if="loading" />

          <div class="text-center mt-4">
            <button
              type="submit"
              class="btn btn-dark btn-lg login-btn"
              :disabled="loading"
            >
              Login
            </button>
          </div>
        </form>

        <p class="mt-3 text-center">
          Don't have an account?
          <router-link to="/register" class="text-decoration-none"
            >Sign up</router-link
          >
        </p>
      </div>
    </div>

    <AppFooter />
  </div>
</template>

<script>
import axios from "axios";
import { useToast } from "vue-toastification";
import NavBar from "@/components/NavBar.vue";
import AppFooter from "@/components/AppFooter.vue";
import BaseLoader from "@/components/BaseLoader.vue";
export default {
  name: "LoginPage",
  components: {
    AppFooter,
    NavBar,
    BaseLoader,
  },
  data() {
    return {
      username: "",
      password: "",
      loading: false,
      error: null,
      success: null,
    };
  },
  methods: {
    async handleLogin() {
      const toast = useToast();
      this.loading = true;

      if (!this.username || !this.password) {
        toast.error("Please enter both username and password.");
        this.loading = false;
        return;
      }

      try {
        const response = await axios.post("/auth/login", {
          username: this.username.trim().toLowerCase(),
          password: this.password,
        });

        const data = response?.data;
        if (!data || !data.access_token || !data.user?.role) {
          throw new Error("Invalid server response.");
        }

        // Vuex action to store token and user data
        this.$store.dispatch("login", {
          token: data.access_token,
          user: {
            id: data.user.id,
            username: data.user.username,
            name: data.user.name,
            role: data.user.role.toLowerCase(),
          },
        });

        toast.success("Login successful!");
        setTimeout(() => {
          if (data.user.role === "admin") {
            this.$router.push("/admin/dashboard");
          } else {
            this.$router.push("/user/dashboard");
          }
        }, 1200);
      } catch (error) {
        const errMsg =
          error.response?.data?.message || "Login failed. Please try again.";
        toast.error(errMsg);
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.login-wrapper {
  min-height: 100vh;
}
.login-page {
  background: no-repeat center center/cover;
}
.login-card {
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  width: 100%;
  max-width: 550px;
}

.login-page {
  background-color: #ffffff;
}

input:focus,
button:focus {
  box-shadow: none;
  outline: none;
}

.btn-dark {
  background-color: #5c4033;
  color: #fff;
  padding: 10px 30px;
  font-size: 1rem;
  border: 1px solid transparent;
  transition: all 0.3s ease;
}

.btn-dark:hover {
  background-color: transparent;
  color: #5c4033;
  border: 1px solid #5c4033;
  transition: all 0.3s ease;
}
</style>
