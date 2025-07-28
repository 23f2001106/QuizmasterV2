import UserDashboard from "../views/user/UserDashboard.vue";
import UserProfile from "../views/user/UserProfile.vue";
import UserSettings from "../views/user/UserSettings.vue";
import QuizPage from "../views/user/QuizPage.vue";
import ScoresPage from "../views/user/ScoresPage.vue";
import UserSummary from "../views/user/UserSummary.vue";
import TakeQuiz from "../views/user/TakeQuiz.vue";
import StartQuiz from "../views/user/StartQuiz.vue";
import QuizResult from "../views/user/QuizResult.vue";

const userRoutes = [
  {
    path: "/user/dashboard",
    name: "UserDashboard",
    component: UserDashboard,
  },
  {
    path: "/user/profile",
    name: "UserProfile",
    component: UserProfile,
  },
  {
    path: "/user/settings",
    name: "UserSettings",
    component: UserSettings,
  },
  {
    path: "/user/quizzes",
    name: "QuizPage",
    component: QuizPage,
  },
  {
    path: "/user/scores",
    name: "ScoresPage",
    component: ScoresPage,
  },
  {
    path: "/user/summary",
    name: "UserSummary",
    component: UserSummary,
  },
  {
    path: "/quiz/:quizId",
    name: "TakeQuiz",
    component: TakeQuiz,
  },
  {
    path: "/quiz/:quizId/start",
    name: "StartQuiz",
    component: StartQuiz,
  },
  {
    path: "/quiz/:quizId/result",
    name: "QuizResult",
    component: QuizResult,
  },
];

export default userRoutes;
