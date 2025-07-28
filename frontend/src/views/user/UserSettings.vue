<template>
  <div class="settings-page d-flex flex-column min-vh-100">
    <!-- Main Layout -->
    <div class="flex-grow-1 d-flex">
      <!-- Sidebar -->
      <aside class="settings-sidebar border-end">
        <SideBar />
      </aside>

      <!-- Content Area -->
      <main class="settings-content flex-grow-1 p-4">
        <div class="header mb-4">
          <h1 class="title">User Settings</h1>
        </div>

        <!-- Loader or Settings Sections -->
        <BaseLoader v-if="loading" />
        <div v-else class="d-flex flex-column gap-4">
          <EditProfile :user="user" @updated="fetchUser" />
          <NotificationSettings :user="user" @updated="fetchUser" />
          <DeleteAccount :userId="user.id" />
        </div>
      </main>
    </div>

    <!-- Footer -->
    <AppFooter />
  </div>
</template>

<script>
import axios from "axios";
import EditProfile from "@/components/user/EditProfile.vue";
import NotificationSettings from "@/components/user/NotificationSettings.vue";
import DeleteAccount from "@/components/user/DeleteAccount.vue";
import SideBar from "@/components/user/SideBar.vue";
import AppFooter from "@/components/AppFooter.vue";
import BaseLoader from "@/components/BaseLoader.vue";

export default {
  name: "UserSettings",
  components: {
    EditProfile,
    NotificationSettings,
    DeleteAccount,
    SideBar,
    AppFooter,
    BaseLoader,
  },
  data() {
    return {
      user: null,
      loading: true,
    };
  },
  methods: {
    async fetchUser() {
      try {
        this.loading = true;
        const res = await axios.get("/user/profile");
        this.user = res.data;
      } catch (err) {
        console.error("Failed to fetch user:", err);
      } finally {
        this.loading = false;
      }
    },
  },
  mounted() {
    this.fetchUser();
  },
};
</script>
