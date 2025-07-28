<template>
  <div
    class="alert text-center my-3"
    :class="{
      'alert-danger': type === 'error',
      'alert-success': type === 'success',
      'alert-warning': type === 'warning',
    }"
    role="alert"
  >
    {{ message }}
  </div>
</template>

<script>
export default {
  name: "BaseMessage",
  props: {
    type: {
      type: String,
      default: "error", // or "success", "warning"
    },
    message: {
      type: String,
      required: true,
    },
  },
};
</script>
