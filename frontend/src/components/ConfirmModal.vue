<template>
  <div class="modal-backdrop" @click.self="cancel">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">{{ title }}</h5>
          <button type="button" class="btn-close" @click="cancel"></button>
        </div>
        <div class="modal-body">
          <p>{{ message }}</p>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="cancel">Cancel</button>
          <button class="btn btn-danger" @click="confirm">Confirm</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ConfirmModal",
  props: {
    title: String,
    message: String,
  },
  methods: {
    confirm() {
      this.$emit("confirm");
    },
    cancel() {
      this.$emit("cancel");
    },
  },
};
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1050;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.65); /* darker backdrop */
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-dialog {
  width: 90%;
  max-width: 500px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  background-color: #fff;
}

.modal-content {
  border: none;
  background-color: #fefefe;
}

.modal-header {
  background-color: #f5f7fa;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e1e5eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #2d2f33;
  margin: 0;
}

.modal-body {
  padding: 1.5rem 1.5rem;
  font-size: 1rem;
  color: #333;
  text-align: left;
}

.modal-footer {
  padding: 0.5rem 1.5rem;
  background-color: #f5f7fa;
  border-top: 1px solid #e1e5eb;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.btn {
  border-radius: 6px;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border: none;
  cursor: pointer;
}

.btn-secondary {
  background-color: #dee2e6;
  color: #495057;
}

.btn-secondary:hover {
  background-color: #ced4da;
  color: #343a40;
}

.btn-danger {
  background-color: #dc3545;
  color: #fff;
}

.btn-danger:hover {
  background-color: #c82333;
}
</style>
