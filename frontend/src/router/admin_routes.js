import AdminDashboard from "../views/admin/AdminDashboard.vue";
import AdminSummary from "../views/admin/AdminSummary.vue";
import UsersPage from "../views/admin/UsersPage.vue";
import SubjectPage from "../views/admin/SubjectPage.vue";
import QuizPage from "../views/admin/QuizPage.vue";
import SearchPage from "../views/admin/SearchPage.vue";

const adminRoutes = [
  {
    path: "/admin/dashboard",
    name: "Admin Dashboard",
    component: AdminDashboard,
  },
  {
    path: "/admin/summary",
    name: "Admin Summary",
    component: AdminSummary,
  },
  {
    path: "/admin/users",
    name: "Users Page ",
    component: UsersPage,
  },
  {
    path: "/admin/subjects",
    name: "Subject Page ",
    component: SubjectPage,
  },
  {
    path: "/admin/quizzes",
    name: "Quiz Page ",
    component: QuizPage,
  },
  {
    path: "/admin/search",
    name: "Search Page ",
    component: SearchPage,
  },
];

export default adminRoutes;
