import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import axios from "axios";
import Toast from "vue-toastification";

import "vue-toastification/dist/index.css";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";
import "bootstrap-icons/font/bootstrap-icons.css";

axios.defaults.baseURL = "/api";

axios.interceptors.request.use((config) => {
  const token = store.state.authToken || localStorage.getItem("authToken");
  // console.log("Sending request with token:", token);
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  console.log("Axios Request:", config.method.toUpperCase(), config.url);
  return config;
});

axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      store.dispatch("logout");
      window.location.href = "/login";
    }

    return Promise.reject(error);
  }
);

store.dispatch("tryAutoLogin").then(() => {
  const app = createApp(App);

  app.use(store);
  app.use(router);
  app.use(Toast, {
    position: "top-right",
    timeout: 3000,
    closeOnClick: true,
    pauseOnHover: true,
    draggable: true,
    showCloseButtonOnHover: false,
  });

  app.mount("#app");
});
