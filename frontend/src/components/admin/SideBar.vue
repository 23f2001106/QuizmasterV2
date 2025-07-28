<template>
  <aside :class="['sidebar', { collapsed }]">
    <div class="top-section">
      <router-link to="/admin/dashboard" class="brand">
        <img src="/q.jpg" alt="QuizMaster Logo" class="logo" />
        <span class="brand-text" v-if="!collapsed">Quizmaster</span>
      </router-link>

      <button class="toggle-btn" @click="toggleSidebar">
        <ChevronLeftIcon v-if="!collapsed" class="icon toggle-icon" />
        <ChevronRightIcon v-else class="icon toggle-icon" />
      </button>
    </div>

    <nav class="nav-links">
      <router-link to="/admin/dashboard" class="nav-item">
        <HomeIcon class="icon" />
        <span class="label" v-if="!collapsed">Dashboard</span>
      </router-link>

      <router-link to="/admin/users" class="nav-item">
        <UserIcon class="icon" />
        <span class="label" v-if="!collapsed">Users</span>
      </router-link>

      <router-link to="/admin/subjects" class="nav-item">
        <BookOpenIcon class="icon" />
        <span class="label" v-if="!collapsed">Subjects</span>
      </router-link>

      <router-link to="/admin/quizzes" class="nav-item">
        <ClipboardDocumentListIcon class="icon" />
        <span class="label" v-if="!collapsed">Quizzes</span>
      </router-link>

      <router-link to="/admin/summary" class="nav-item">
        <ChartPieIcon class="icon" />
        <span class="label" v-if="!collapsed">Summary</span>
      </router-link>

      <div class="nav-item" @click="handleLogout">
        <PowerIcon class="icon" />
        <span class="label" v-if="!collapsed">Logout</span>
      </div>
    </nav>
  </aside>
  <ConfirmModal
    v-if="confirmModal.show"
    :title="confirmModal.title"
    :message="confirmModal.message"
    @confirm="handleConfirm"
    @cancel="handleCancel"
  />
</template>

<script>
import { mapActions } from "vuex";
import { useToast } from "vue-toastification";
import ConfirmModal from "../ConfirmModal.vue";
import {
  HomeIcon,
  UserIcon,
  BookOpenIcon,
  ChartPieIcon,
  ClipboardDocumentListIcon,
  PowerIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
} from "@heroicons/vue/24/outline";

export default {
  name: "SideBar",
  components: {
    HomeIcon,
    UserIcon,
    BookOpenIcon,
    ChartPieIcon,
    ClipboardDocumentListIcon,
    PowerIcon,
    ChevronLeftIcon,
    ChevronRightIcon,
    ConfirmModal,
  },
  data() {
    return {
      collapsed: false,
      confirmModal: {
        show: false,
        title: "Confirm Logout",
        message: "Are you sure you want to log out?",
        onConfirm: null,
      },
    };
  },
  mounted() {
    const stored = localStorage.getItem("sidebarCollapsed");
    this.collapsed = stored === "true";
  },
  methods: {
    toggleSidebar() {
      this.collapsed = !this.collapsed;
      localStorage.setItem("sidebarCollapsed", this.collapsed);
    },
    openConfirmModal(message, onConfirm) {
      this.confirmModal.message = message;
      this.confirmModal.onConfirm = onConfirm;
      this.confirmModal.show = true;
    },

    handleConfirm() {
      if (typeof this.confirmModal.onConfirm === "function") {
        this.confirmModal.onConfirm();
      }
      this.confirmModal.show = false;
    },

    handleCancel() {
      this.confirmModal.show = false;
    },
    ...mapActions(["logout"]),
    handleLogout() {
      const toast = useToast();

      this.openConfirmModal("Are you sure you want to log out?", () => {
        this.logout()
          .then(() => {
            this.$router.push("/login");
            toast.success("You have been logged out successfully.");
          })
          .catch((err) => {
            console.error("Logout error:", err);
            toast.error("An error occurred while logging out.");
          });
      });
    },
  },
};
</script>

<style scoped>
.sidebar {
  width: 240px;
  background-color: #f0f2f5;
  color: #333;
  display: flex;
  flex-direction: column;
  padding: 1rem 0.5rem;
  transition: width 0.3s ease;
  border-right: 1px solid #ddd;
  min-height: 100vh;
}

.sidebar.collapsed {
  width: 80px;
}

.top-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 0.5rem 1rem;
  border-bottom: 1px solid #ccc;
}

.brand {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #333;
  text-decoration: none;
}

.logo {
  width: 32px;
  height: 32px;
  border-radius: 4px;
}

.brand-text {
  font-size: 1.1rem;
}

.toggle-btn {
  background: none;
  border: none;
  color: #666;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0.2rem;
}

.nav-links {
  display: flex;
  flex-direction: column;
  margin-top: 1rem;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 0.75rem 1rem;
  text-decoration: none;
  color: #444;
  border-radius: 6px;
  transition: all 0.2s ease;
  cursor: pointer;
}

.nav-item:hover {
  background-color: #e0e3e8;
}

.label {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  transition: opacity 0.2s ease;
  margin-left: 0.75rem;
}

.sidebar.collapsed .label {
  opacity: 0;
  pointer-events: none;
}

.icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.toggle-icon {
  width: 18px;
  height: 18px;
}
</style>
