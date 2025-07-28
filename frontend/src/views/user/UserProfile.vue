<template>
  <div class="profile-layout">
    <SideBar />

    <div class="main-content">
      <BaseLoader v-if="loading" />

      <div v-else class="profile-container">
        <div class="profile-header">
          <h2 class="title">User Profile</h2>
          <router-link to="/user/settings" class="edit-button"
            >Edit Profile</router-link
          >
        </div>

        <div class="profile-card">
          <div
            class="profile-item"
            v-for="(value, label) in profileFields"
            :key="label"
          >
            <strong>{{ formatLabel(label) }}</strong>
            <span>
              <template v-if="label === 'is_verified'">
                <span
                  class="badge"
                  :class="value === 'Yes' ? 'verified' : 'unverified'"
                >
                  {{ value }}
                </span>
              </template>

              <template v-else-if="label === 'status'">
                <span
                  class="badge"
                  :class="value === 'active' ? 'active' : 'inactive'"
                >
                  {{ value }}
                </span>
              </template>

              <template v-else>
                {{ formatValue(label, value) }}
              </template>
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
  <AppFooter />
</template>

<script>
import axios from "axios";
import SideBar from "@/components/user/SideBar.vue";
import AppFooter from "@/components/AppFooter.vue";
import BaseLoader from "@/components/BaseLoader.vue";

export default {
  name: "UserProfile",
  components: {
    SideBar,
    AppFooter,
    BaseLoader,
  },
  data() {
    return {
      profileData: {},
      loading: true,
    };
  },
  computed: {
    profileFields() {
      return {
        username: this.profileData.username,
        full_name: this.profileData.full_name,
        qualification: this.profileData.qualification || "N/A",
        dob: this.profileData.dob ? this.profileData.dob : "N/A",
        role: this.profileData.role,
        status: this.profileData.status,
        is_verified: this.profileData.is_verified ? "Yes" : "No",
        created_at: this.profileData.created_at,
        last_login: this.profileData.last_login || "Never",
      };
    },
  },
  mounted() {
    this.fetchProfile();
  },
  methods: {
    async fetchProfile() {
      try {
        const res = await axios.get("/user/profile");
        this.profileData = res.data;
      } catch (err) {
        console.error("Failed to fetch profile:", err);
      } finally {
        this.loading = false;
      }
    },
    formatLabel(key) {
      return key.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
    },
    formatValue(key, value) {
      if (["created_at", "last_login", "dob"].includes(key)) {
        if (!value) return "N/A";

        const date = new Date(value);
        if (isNaN(date.getTime())) return "N/A";

        return date.toLocaleDateString();
      }
      return value ?? "N/A";
    },
  },
};
</script>

<style scoped>
.profile-layout {
  display: flex;
  min-height: 100vh;
  background-color: #f4f7fa;
}

.main-content {
  flex: 1;
  padding: 2rem;
  display: flex;
  flex-direction: column;
}

.profile-container {
  width: 100%;
  max-width: 900px;
  margin: auto;
  background: #ffffff;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.06);
}

.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.title {
  font-size: 1.8rem;
  font-weight: bold;
  color: #2c3e50;
}

.edit-button {
  background-color: #3498db;
  color: white;
  padding: 0.5rem 1.2rem;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 500;
  transition: background-color 0.3s ease;
}

.edit-button:hover {
  background-color: #2980b9;
}

.profile-card {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.profile-item {
  display: flex;
  flex-direction: column;
  font-size: 1rem;
  color: #34495e;
}

.profile-item strong {
  font-weight: 600;
  margin-bottom: 6px;
  color: #2d3436;
}

.badge {
  display: inline-block;
  padding: 0.3em 0.8em;
  font-size: 0.8rem;
  border-radius: 12px;
  font-weight: 600;
  color: white;
  text-align: center;
  min-width: 60px;
}

.verified {
  background-color: #2ecc71;
}

.unverified {
  background-color: #e74c3c;
}

.active {
  background-color: #24cfb2;
}

.inactive {
  background-color: #e67e22;
}

@media (max-width: 768px) {
  .main-content {
    padding: 1rem;
  }

  .profile-container {
    padding: 1.5rem;
  }

  .profile-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .edit-button {
    align-self: flex-end;
  }
}
</style>
