<template>
  <div class="otp-verification card shadow p-4">
    <h3 class="mb-2 text-center fw-bold">Verify Your Email</h3>
    <p class="text-muted text-center mb-4">
      Please enter the 6-digit OTP sent to your email address.
    </p>

    <form @submit.prevent="submitOtp">
      <div class="mb-4">
        <label for="otp" class="form-label">OTP</label>
        <input
          v-model="otp"
          type="text"
          id="otp"
          class="form-control otp-input"
          placeholder="Enter 6-digit OTP"
          inputmode="numeric"
          pattern="\d{6}"
          maxlength="6"
          required
        />
      </div>

      <div class="d-grid">
        <button type="submit" class="btn btn-primary" :disabled="loading">
          Verify
        </button>
      </div>
    </form>

    <div class="text-center mt-3">
      <button
        class="btn btn-link resend-btn"
        @click="resendOtp"
        :disabled="resendDisabled || loading"
      >
        Resend OTP <span v-if="cooldown">({{ cooldown }}s)</span>
      </button>
    </div>

    <BaseLoader v-if="loading" />
  </div>
</template>

<script>
import axios from "axios";
import { useToast } from "vue-toastification";
import BaseLoader from "../BaseLoader.vue";

export default {
  name: "OtpVerification",
  components: {
    BaseLoader,
  },
  props: {
    userId: {
      type: Number,
      required: true,
    },
    context: {
      type: String,
      required: true, // 'register', 'reset', 'delete'
    },
    endpoint: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      otp: "",
      error: null,
      success: null,
      cooldown: 0,
      resendDisabled: false,
      loading: false,
    };
  },
  computed: {
    title() {
      switch (this.context) {
        case "register":
          return "Verify Your Email";
        case "reset":
          return "Reset Password Verification";
        case "delete":
          return "Confirm Account Deletion";
        default:
          return "OTP Verification";
      }
    },
    description() {
      switch (this.context) {
        case "register":
          return "Please enter the 6-digit OTP sent to your email to verify your account.";
        case "reset":
          return "Enter the OTP sent to your email to proceed with password reset.";
        case "delete":
          return "To delete your account, enter the OTP sent to your registered email.";
        default:
          return "Enter the 6-digit OTP sent to your email.";
      }
    },
  },
  methods: {
    async submitOtp() {
      const toast = useToast();
      this.loading = true;

      try {
        const payload = {
          otp: this.otp,
          ...(this.userId ? { user_id: this.userId } : {}),
        };

        const response =
          this.context === "delete"
            ? await axios.delete(this.endpoint, { data: payload })
            : await axios.post(this.endpoint, payload);

        toast.success("OTP verified successfully!");
        this.$emit("verified", response.data); // Notify parent
      } catch (err) {
        const errorMsg =
          err.response?.data?.message ||
          err.response?.data?.error ||
          "OTP verification failed.";
        toast.error(errorMsg);
      } finally {
        this.loading = false;
      }
    },
    async resendOtp() {
      const toast = useToast();
      this.loading = true;
      this.resendDisabled = true;
      try {
        await axios.post("/auth/resend-otp", {
          user_id: this.userId,
          context: this.context,
        });
        toast.success("OTP resent successfully!");
        this.cooldown = 60;
        this.countdown();
      } catch (err) {
        if (err.response?.status === 429) {
          const retrySeconds = parseInt(err.response?.data?.cooldown, 10);
          this.cooldown = Math.max(retrySeconds || 60, 1);
          this.error =
            err.response.data.message || "Please wait before retrying.";
          this.countdown();
        } else {
          const errorMsg =
            err.response?.data?.message || "Failed to resend OTP.";
          toast.error(errorMsg);
          this.resendDisabled = false;
        }
      } finally {
        this.loading = false;
      }
    },
    countdown() {
      const interval = setInterval(() => {
        if (this.cooldown > 0) {
          this.cooldown--;
        } else {
          clearInterval(interval);
          this.resendDisabled = false;
        }
      }, 1000);
    },
  },
};
</script>

<style scoped>
.otp-verification {
  max-width: 400px;
  margin: 30px auto;
  background-color: #ffffff;
  border-radius: 10px;
}

.otp-input {
  font-size: 1.2rem;
  text-align: center;
  letter-spacing: 4px;
  padding: 10px;
}

.btn-primary {
  background-color: #1dd8e2;
  border: none;
  font-weight: 600;
  transition: background-color 0.3s ease;
}
.btn-primary:hover {
  background-color: #00b6bf;
}

.resend-btn {
  color: #00a7b0;
  font-weight: 500;
  text-decoration: none;
}
.resend-btn:disabled {
  color: #aaa;
  pointer-events: none;
}
</style>
