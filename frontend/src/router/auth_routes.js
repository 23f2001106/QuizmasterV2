import LoginPage from "../views/auth/LoginPage.vue";
import RegisterPage from "../views/auth/RegisterPage.vue";
import ResetPassword from "../views/auth/ResetPassword.vue";

const authRoutes = [
  {
    path: "/login",
    name: "Login",
    component: LoginPage,
  },
  {
    path: "/register",
    name: "Register",
    component: RegisterPage,
  },
  {
    path: "/reset-password",
    name: "Reset Password",
    component: ResetPassword,
  },
];

export default authRoutes;
