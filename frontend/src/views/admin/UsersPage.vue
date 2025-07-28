<template>
  <div class="page-layout">
    <SideBar />

    <div class="main-content">
      <!-- Loader -->
      <BaseLoader v-if="loading" />

      <div v-else>
        <!-- Welcome -->
        <header class="page-header">
          <h2>Welcome, Admin</h2>
        </header>

        <div class="heading p-3"><h1>Users</h1></div>

        <div v-if="users.length === 0" class="alert alert-info text-center">
          No users found.
        </div>

        <!-- User Table -->
        <div v-else class="table-responsive">
          <table class="table table-striped align-middle">
            <thead class="header text-center">
              <tr>
                <th>ID</th>
                <th>Username</th>
                <th>Role</th>
                <th>Status</th>
                <th>Verified</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in users" :key="user.id" class="text-center">
                <td>{{ user.id }}</td>
                <td>{{ user.username }}</td>
                <td>{{ user.role }}</td>
                <td>
                  <button
                    class="btn status-btn btn-sm"
                    :class="{
                      'btn-success': user.status === 'ACTIVE',
                      'btn-warning': user.status === 'INACTIVE',
                      'btn-danger': user.status === 'SUSPENDED',
                    }"
                    @click="toggleStatus(user)"
                  >
                    {{ user.status }}
                  </button>
                </td>
                <td>
                  <span
                    :class="{
                      'text-success fw-bold': user.is_verified,
                      'text-danger fw-bold': !user.is_verified,
                    }"
                  >
                    {{ user.is_verified ? "Yes" : "No" }}
                  </span>
                </td>
                <td>
                  <button class="view-btn btn" @click="viewUser(user)">
                    View Details
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>

  <!-- User Detail Modal -->
  <FormModal
    v-if="selectedUser"
    :title="'User Details'"
    :formData="formattedUser"
    :fields="userDetailFields"
    :readOnly="true"
    @close="closeModal"
  />

  <ConfirmModal
    v-if="confirmData"
    :title="confirmData.title"
    :message="confirmData.message"
    @confirm="confirmStatusChange"
    @cancel="confirmData = null"
  />

  <AppFooter />
</template>

<script>
import axios from "axios";
import SideBar from "@/components/admin/SideBar.vue";
import AppFooter from "@/components/AppFooter.vue";
import BaseLoader from "@/components/BaseLoader.vue";
import FormModal from "@/components/admin/FormModal.vue";
import ConfirmModal from "@/components/ConfirmModal.vue";
import { useToast } from "vue-toastification";

export default {
  name: "UsersPage",
  components: {
    SideBar,
    AppFooter,
    BaseLoader,
    FormModal,
    ConfirmModal,
  },
  data() {
    return {
      loading: true,
      users: [],
      selectedUser: null,
      confirmData: null,
      userDetailFields: [
        { name: "id", label: "ID", type: "number", disabled: true },
        { name: "username", label: "Username", type: "text" },
        { name: "full_name", label: "Full Name", type: "text" },
        { name: "qualification", label: "Qualification", type: "text" },
        { name: "dob", label: "DOB", type: "date" },
        { name: "role", label: "Role", type: "text" },
        { name: "status", label: "Status", type: "text" },
        { name: "created_at", label: "Created At", type: "text" },
        { name: "last_login", label: "Last Login", type: "text" },
        {
          name: "notifications_enabled",
          label: "Notifications Enabled",
          type: "text",
        },
        {
          name: "preferred_reminder_time",
          label: "Preferred Reminder Time",
          type: "text",
        },
        {
          name: "is_verified",
          label: "Verified",
          type: "text",
        },
      ],
    };
  },
  methods: {
    async fetchUsers() {
      try {
        const response = await axios.get("/admin/users");
        this.users = response.data;
      } catch (error) {
        console.error("Error fetching users:", error);
      } finally {
        this.loading = false;
      }
    },
    formatDate(dateStr) {
      if (!dateStr) return "N/A";
      const date = new Date(dateStr);
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, "0");
      const day = String(date.getDate()).padStart(2, "0");
      const hours = date.getHours();
      const minutes = String(date.getMinutes()).padStart(2, "0");
      return `${year}-${month}-${day}, ${hours}:${minutes}`;
    },
    viewUser(user) {
      this.selectedUser = {
        ...user,
        notifications_enabled: user.notifications_enabled ? "Yes" : "No",
        is_verified: user.is_verified ? "Yes" : "No",
      };
    },
    closeModal() {
      this.selectedUser = null;
    },
    toggleStatus(user) {
      let newStatus;
      switch (user.status) {
        case "ACTIVE":
          newStatus = "SUSPENDED";
          break;
        case "SUSPENDED":
        case "INACTIVE":
          newStatus = "ACTIVE";
          break;
        default:
          newStatus = "SUSPENDED";
      }
      this.confirmData = {
        user,
        newStatus,
        title: "Confirm Status Change",
        message: `Are you sure you want to change status of "${user.username}" to "${newStatus}"?`,
      };
    },
    async confirmStatusChange() {
      const toast = useToast();
      const { user, newStatus } = this.confirmData;
      try {
        await axios.put(`/admin/users/${user.id}/status`, {
          status: newStatus,
        });
        user.status = newStatus;
        toast.success(`Status changed to ${newStatus} for ${user.username}`);
      } catch (error) {
        toast.error("Error updating user status");
        console.error(error);
      } finally {
        this.confirmData = null;
      }
    },
  },
  computed: {
    formattedUser() {
      if (!this.selectedUser) return null;

      return {
        ...this.selectedUser,
        notifications_enabled: this.selectedUser.notifications_enabled
          ? "Yes"
          : "No",
        is_verified: this.selectedUser.is_verified ? "Yes" : "No",
        created_at: this.formatDate(this.selectedUser.created_at),
        last_login: this.formatDate(this.selectedUser.last_login),
      };
    },
  },

  mounted() {
    this.fetchUsers();
  },
};
</script>

<style scoped>
.page-layout {
  display: flex;
  min-height: 100vh;
  background-color: #f9f9f9;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 1.5rem;
}

.page-header {
  margin-bottom: 2rem;
  font-size: 1.5rem;
  font-weight: 600;
}

.table-responsive {
  overflow-x: auto;
}

.table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  font-size: 14px;
  border: 1px solid #dee2e6;
}

.table thead th {
  background-color: #292147;
  color: #ffffff;
  padding: 10px 12px;
}

.table tbody td {
  padding: 10px 12px;
  vertical-align: middle;
  border-top: 1px solid #dee2e6;
  background-color: transparent;
  transition: background-color 0.3s ease;
  border-right: 1px solid #dee2e6;
}

.table tbody tr:hover {
  background-color: #f1f5fb !important;
  cursor: pointer;
}

.table tbody td:hover {
  background-color: #f7f9fc;
  cursor: pointer;
}

.view-btn {
  background-color: rgb(32, 219, 244);
  color: white;
}

.view-btn:hover {
  background-color: rgb(29, 205, 228);
  color: white;
}

.status-btn:hover {
  opacity: 0.9;
}

.modal {
  z-index: 1050;
}
</style>
