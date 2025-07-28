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

export default {
  props: ["user"],
  data() {
    return {
      form: {
        full_name: this.user.full_name,
        qualification: this.user.qualification,
        dob: this.user.dob ? this.user.dob.slice(0, 10) : null,
      },
    };
  },
  methods: {
    async updateProfile() {
      await axios.put("/user/settings", this.form);
      this.$emit("updated");
    },
  },
};
</script>
