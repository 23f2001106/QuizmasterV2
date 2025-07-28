<template>
  <div class="reset-wrapper d-flex flex-column min-vh-100">
    <div
      class="reset-password-page flex-grow-1 d-flex justify-content-center align-items-center"
    >
      <!-- Back Arrow -->
      <button
        class="btn btn-link p-0 position-absolute top-0 start-0 m-3 fs-3 text-muted back-arrow"
        @click="goBack"
        aria-label="Back to Login"
      >
        <i class="bi bi-arrow-left"></i>
      </button>
      <div
        v-if="!otpSent"
        class="reset-card p-4 shadow rounded position-relative"
      >
        <h2 class="text-center mb-4">Reset Password</h2>
        <div>
          <form
            @submit.prevent="submitResetRequest"
            class="w-100"
            style="max-width: 400px; margin: auto"
          >
            <div class="mb-3">
              <label class="form-label">Username (email)</label>
              <input
                v-model="username"
                type="email"
                class="form-control"
                placeholder="Username"
                required
              />
            </div>

            <div class="mb-3">
              <label class="form-label">New Password</label>
              <input
                v-model="newPassword"
                type="password"
                class="form-control"
                placeholder="New Password"
                required
              />
            </div>

            <div class="mb-3">
              <label class="form-label">Confirm Password</label>
              <input
                v-model="confirmPassword"
                type="password"
                class="form-control"
                placeholder="Re-enter Password"
                required
              />
            </div>

            <div
              v-if="confirmPassword && confirmPassword !== newPassword"
              class="text-danger small mt-1"
            >
              Passwords do not match.
            </div>

            <div class="text-center">
              <button
                class="btn btn-custom-primary"
                type="submit"
                :disabled="loading"
              >
                <BaseLoader v-if="loading" /> Continue
              </button>
            </div>
          </form>
        </div>
      </div>
      <!-- OTP Component -->
      <OtpVerification
        v-else
        :user-id="userId"
        endpoint="/auth/verify-password-reset"
        context="reset"
        @verified="onVerified"
      />
    </div>
    <AppFooter />
  </div>
</template>

<script>
import axios from "axios";
import { useToast } from "vue-toastification";
import OtpVerification from "@/components/auth/OtpVerification.vue";
import BaseLoader from "@/components/BaseLoader.vue";
import AppFooter from "@/components/AppFooter.vue";

export default {
  name: "ResetPassword",
  components: {
    OtpVerification,
    BaseLoader,
    AppFooter,
  },
  data() {
    return {
      username: "",
      newPassword: "",
      confirmPassword: "",
      userId: null,
      otpSent: false,
      error: null,
      loading: false,
    };
  },
  methods: {
    async submitResetRequest() {
      this.loading = true;
      const toast = useToast();

      try {
        const res = await axios.post("/auth/request-password-reset", {
          username: this.username.trim().toLowerCase(),
          new_password: this.newPassword,
          confirm_password: this.confirmPassword,
        });
        this.userId = res.data.user_id;
        this.otpSent = true;
      } catch (err) {
        const message =
          err.response?.data?.message || "Failed to request password reset.";
        toast.error(message);
      } finally {
        this.loading = false;
      }
    },
    onVerified() {
      const toast = useToast();
      toast.success("Password reset successful. You can now log in.");
      this.$router.push("/login");
    },
    goBack() {
      this.username = "";
      this.newPassword = "";
      this.confirmPassword = "";
      this.userId = null;
      this.otpSent = false;
      this.error = null;
      this.$router.push("/login");
    },
  },
};
</script>

<style scoped>
.reset-password-page {
  background: linear-gradient(to right, #eef2f3, #ffffff);
}

.reset-card {
  background-color: #ffffff;
  border: 1px solid #e3e3e3;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05);
  width: 100%;
  max-width: 550px;
  position: relative;
}

h2 {
  font-weight: 600;
  font-size: 1.8rem;
  color: #333;
}

.form-label {
  font-weight: 500;
  color: #555;
}

.form-control {
  border-radius: 8px;
  border: 1px solid #ccc;
  transition: border-color 0.3s, box-shadow 0.3s;
}

.form-control:focus {
  border-color: #5a9bd5;
  box-shadow: 0 0 0 0.2rem rgba(90, 155, 213, 0.25);
}

.btn-custom-primary {
  background-color: #3dc2eb;
  color: #fff;
  border: 1px solid transparent;
  padding: 0.5rem 1.5rem;
  border-radius: 6px;
  font-weight: 500;
  transition: background-color 0.3s, box-shadow 0.3s;
}

.btn-custom-primary:hover {
  background-color: #ffffff;
  color: #25b7e4;
  border: 1px solid #25b7e4;
}

.btn-custom-primary:disabled {
  background-color: #b5cde7;
  cursor: not-allowed;
}

.back-arrow {
  padding: 8px;
  transition: all 0.3s ease;
}

.back-arrow i:hover {
  color: #000000;
}
</style>
