<template>
  <div class="card p-4 shadow border-danger">
    <h4 class="text-danger">Delete Account</h4>

    <div v-if="step === 1">
      <p>To delete your account, confirm your password:</p>
      <input
        type="password"
        v-model="password"
        class="form-control mb-3"
        placeholder="Password"
      />
      <button class="btn btn-danger" @click="submitPassword">Continue</button>
    </div>

    <OtpVerification
      v-if="step === 2"
      :userId="userId"
      context="delete"
      endpoint="/user/account-delete"
      @verified="confirmDeletion"
    />

    <BaseMessage v-if="error" :message="error" type="error" />
  </div>
</template>

<script>
import axios from "axios";
import { useToast } from "vue-toastification";
import OtpVerification from "@/components/auth/OtpVerification.vue";
import BaseMessage from "@/components/BaseMessage.vue";

export default {
  components: {
    OtpVerification,
    BaseMessage,
  },
  props: ["userId"],
  data() {
    return {
      password: "",
      step: 1,
      error: null,
    };
  },
  methods: {
    async submitPassword() {
      try {
        await axios.post("/user/account-delete", { password: this.password });
        this.step = 2;
      } catch (err) {
        this.error = err.response?.data?.error || "Incorrect password.";
      }
    },
    async confirmDeletion() {
      const toast = useToast();
      toast.success("Account deleted successfully.");
      await this.$store.dispatch("logout");
      this.$router.push("/login");
    },
  },
};
</script>
