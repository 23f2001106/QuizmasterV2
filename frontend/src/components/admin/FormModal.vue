<template>
  <div class="modal-backdrop" @click.self="close">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">{{ title }}</h5>
          <button type="button" class="btn-close" @click="close"></button>
        </div>

        <form @submit.prevent="submitForm" class="modal-form">
          <div class="modal-body">
            <div v-for="field in fields" :key="field.name" class="mb-3">
              <label :for="field.name" class="form-label">{{
                field.label
              }}</label>

              <input
                v-if="field.type === 'text'"
                :id="field.name"
                v-model="formDataInternal[field.name]"
                type="text"
                class="form-control"
                :readonly="readOnly || field.disabled"
                :required="field.required !== false"
              />

              <input
                v-else-if="field.type === 'number'"
                :id="field.name"
                v-model.number="formDataInternal[field.name]"
                type="number"
                class="form-control"
                :readonly="readOnly || field.disabled"
                :required="field.required !== false"
              />

              <input
                v-else-if="field.type === 'date'"
                :id="field.name"
                v-model="formDataInternal[field.name]"
                type="date"
                class="form-control"
                :readonly="readOnly || field.disabled"
                :required="field.required !== false"
              />

              <input
                v-else-if="field.type === 'duration'"
                :id="field.name"
                v-model="formDataInternal[field.name]"
                type="text"
                class="form-control"
                placeholder="e.g. 02:30:00"
                :readonly="readOnly || field.disabled"
                :required="field.required !== false"
              />

              <textarea
                v-else-if="field.type === 'textarea'"
                :id="field.name"
                v-model="formDataInternal[field.name]"
                class="form-control"
                rows="3"
                :readonly="readOnly || field.disabled"
                :required="field.required !== false"
              ></textarea>

              <select
                v-else-if="field.type === 'select'"
                :id="field.name"
                v-model="formDataInternal[field.name]"
                class="form-select"
                :disabled="readOnly || field.disabled"
                :required="field.required !== false"
              >
                <option
                  v-for="option in field.options"
                  :key="option.value"
                  :value="option.value"
                >
                  {{ option.label }}
                </option>
              </select>

              <input
                v-else
                :id="field.name"
                v-model="formDataInternal[field.name]"
                type="text"
                class="form-control"
                :readonly="readOnly || field.disabled"
              />
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="close">
              Cancel
            </button>
            <button v-if="!readOnly" type="submit" class="btn btn-primary">
              Save
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "FormModal",
  props: {
    title: {
      type: String,
      required: true,
    },
    formData: {
      type: Object,
      default: () => ({}),
    },
    fields: {
      type: Array,
      required: true,
    },
    readOnly: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      formDataInternal: { ...this.formData },
    };
  },
  methods: {
    close() {
      this.$emit("close");
    },
    submitForm() {
      this.$emit("form-submit", { ...this.formDataInternal });
    },
  },
  watch: {
    formData: {
      handler(newVal) {
        this.formDataInternal = { ...newVal };
      },
      deep: true,
      immediate: true,
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
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.modal-dialog {
  width: 90%;
  max-width: 720px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  border-radius: 12px;
  overflow: hidden;
  background-color: #ffffff;
  transition: transform 0.3s ease, opacity 0.3s ease;
}

.modal-content {
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: #fefefe;
  border-radius: 12px;
  border: none;
}

.modal-form {
  display: flex;
  flex-direction: column;
  flex: 1;
  overflow: hidden;
}

.modal-body {
  overflow-y: scroll;
  flex-grow: 1;
  padding: 16px 24px;
  max-height: 60vh;
}

.modal-header,
.modal-footer {
  background-color: #f5f7fa;
  border-bottom: 1px solid #e1e5eb;
  padding: 16px 24px;
}

.modal-footer {
  border-top: 1px solid #e1e5eb;
  justify-content: flex-end;
  gap: 8px;
}

.modal-title {
  font-weight: 600;
  font-size: 1.25rem;
  color: #2d2f33;
}

.form-label {
  font-weight: 500;
  color: #495057;
  padding: 1rem 1rem 0.5rem 1rem;
  display: block;
}

.form-control,
.form-select,
textarea.form-control {
  border: 1px solid #ced4da;
  border-radius: 8px;
  padding: 0.5rem 0.75rem;
  margin: 0 1rem 1rem 1rem;
  transition: border-color 0.2s ease-in-out;
  background-color: #fff;
  color: #212529;
  width: calc(100% - 2rem);
  box-sizing: border-box;
}

.form-control:focus,
.form-select:focus {
  border-color: #86b7fe;
  outline: none;
  box-shadow: 0 0 0 0.15rem rgba(13, 110, 253, 0.25);
}

.btn {
  border-radius: 6px;
  font-weight: 500;
  padding: 0.5rem 1rem;
}

.btn-secondary {
  background-color: #dee2e6;
  color: #495057;
  border: 0.5px solid #dee2e6;
}

.btn-secondary:hover {
  background-color: transparent;
  border: 0.5px solid #495057;
  color: #495057;
}

.btn-primary {
  background-color: #28a745;
  border-color: #28a745;
  color: #ffffff;
}

.btn-primary:hover {
  background-color: transparent;
  color: #28a745;
  border-color: #28a745;
}

textarea.form-control {
  resize: vertical;
}
</style>
