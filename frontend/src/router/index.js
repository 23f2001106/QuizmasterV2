import { createRouter, createWebHistory } from "vue-router";
import mainRoutes from "./main_routes";
import authRoutes from "./auth_routes";
import userRoutes from "./user_routes";
import adminRoutes from "./admin_routes";

const routes = [...mainRoutes, ...authRoutes, ...userRoutes, ...adminRoutes];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
