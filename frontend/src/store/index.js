import { createStore } from "vuex";
import axios from "axios";

export default createStore({
  state: {
    authToken: localStorage.getItem("authToken") || "",
    user: JSON.parse(localStorage.getItem("user")) || {
      id: null,
      username: null,
      name: null,
      role: null,
    },
  },
  getters: {
    isAuthenticated: (state) => !!state.authToken,
    isAdmin: (state) => state.user.role === "admin",
  },
  mutations: {
    setAuthToken(state, token) {
      state.authToken = token;
    },
    setUser(state, user) {
      state.user = user;
    },
    clearAuth(state) {
      state.authToken = "";
      state.user = {
        id: null,
        username: null,
        name: null,
        role: null,
      };
    },
  },
  actions: {
    login({ commit }, { token, user }) {
      commit("setAuthToken", token);
      commit("setUser", user);

      localStorage.setItem("authToken", token);
      localStorage.setItem("user", JSON.stringify(user));

      // Set default axios header for authenticated requests
      axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
    },
    logout({ commit }) {
      return new Promise((resolve, reject) => {
        try {
          commit("clearAuth");
          localStorage.removeItem("authToken");
          localStorage.removeItem("user");
          delete axios.defaults.headers.common["Authorization"];
          resolve();
        } catch (error) {
          reject(error);
        }
      });
    },
    tryAutoLogin({ commit }) {
      const token = localStorage.getItem("authToken");
      const user = JSON.parse(localStorage.getItem("user"));
      if (token && user) {
        commit("setAuthToken", token);
        commit("setUser", user);
        axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
      }
    },
  },
});
