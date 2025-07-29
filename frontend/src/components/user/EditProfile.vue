<template>
  <form @submit.prevent="updateProfile" class="card p-4 shadow">
    <h4>Edit Profile</h4>

    <div class="mb-3">
      <label class="form-label">Username</label>
      <input class="form-control" :value="user.username" disabled />
    </div>

    <div class="mb-3">
      <label class="form-label">Full Name</label>
      <input class="form-control" v-model="form.full_name" />
    </div>

    <div class="mb-3">
      <label class="form-label">Qualification</label>
      <input class="form-control" v-model="form.qualification" />
    </div>

    <div class="mb-3">
      <label class="form-label">Date of Birth</label>
      <input type="date" class="form-control" v-model="form.dob" />
    </div>

    <div class="mb-3">
      <label class="form-label">Role</label>
      <input class="form-control" :value="user.role" disabled />
    </div>

    <button type="submit" class="btn btn-primary">Save Changes</button>
  </form>
</template>

<script>
import axios from "axios";
import { useToast } from "vue-toastification";

export default {
  props: ["user"],
  data() {
    return {
      form: {
        full_name: this.user.full_name || "",
        qualification: this.user.qualification || "",
        dob: this.user.dob ? this.user.dob.slice(0, 10) : null,
      },
    };
  },
  methods: {
    async updateProfile() {
      const toast = useToast();
      try {
        const payload = {
          ...this.form,
          full_name: this.form.full_name.trim() || undefined,
          qualification: this.form.qualification.trim() || undefined,
          dob: this.form.dob || undefined,
        };
        await axios.put("/user/settings", payload);
        toast.success("Profile updated!");
        this.$emit("updated");
      } catch (err) {
        if (err.response && err.response.data?.error) {
          toast.error("Error: " + err.response.data.error);
        } else {
          toast.error("An unexpected error occurred.");
        }
        console.error(err);
      }
    },
  },
};
</script>
