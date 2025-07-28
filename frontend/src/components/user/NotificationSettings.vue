<template>
  <div class="card p-4 shadow">
    <h4>Notification Settings</h4>

    <div class="form-check form-switch">
      <input
        class="form-check-input"
        type="checkbox"
        v-model="notifications_enabled"
        @change="updateSettings"
      />
      <label class="form-check-label">Enable Notifications</label>
    </div>

    <div class="mt-3">
      <label class="form-label">Preferred Reminder Time</label>
      <input
        class="form-control"
        type="time"
        v-model="preferred_reminder_time"
        @change="updateSettings"
      />
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  props: ["user"],
  data() {
    return {
      notifications_enabled: this.user.notifications_enabled,
      preferred_reminder_time: this.user.preferred_reminder_time,
    };
  },
  methods: {
    async updateSettings() {
      await axios.patch("/user/settings", {
        notifications_enabled: this.notifications_enabled,
        preferred_reminder_time: this.preferred_reminder_time,
      });
      this.$emit("updated");
    },
  },
};
</script>
