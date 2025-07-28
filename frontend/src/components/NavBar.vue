<template>
  <nav
    class="navbar navbar-expand-lg navbar-light bg-light fixed-top shadow-navbar"
  >
    <div class="container-fluid">
      <router-link class="navbar-brand d-flex align-items-center" to="/">
        <img src="/q.jpg" alt="Home" width="30" height="30" class="me-2" />
        QuizMaster
      </router-link>

      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <a
              class="nav-link"
              href="#"
              @click.prevent="handleNavClick('about')"
              >About</a
            >
          </li>
          <li class="nav-item">
            <a
              class="nav-link"
              href="#"
              @click.prevent="handleNavClick('contact')"
              >Contact</a
            >
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import { Collapse } from "bootstrap";

export default {
  name: "NavBar",
  methods: {
    handleNavClick(sectionId) {
      // Auto-collapse the mobile nav menu if open
      const navCollapse = document.querySelector(".navbar-collapse");
      if (navCollapse.classList.contains("show")) {
        const bsCollapse = new Collapse(navCollapse, { toggle: false });
        bsCollapse.hide();
      }

      // Smooth scroll or route change
      if (this.$route.path !== "/") {
        this.$router.push({ path: "/", query: { scrollTo: sectionId } });
      } else {
        const el = document.getElementById(sectionId);
        if (el) {
          el.scrollIntoView({ behavior: "smooth" });
        }
      }
    },
  },
};
</script>

<style scoped>
.shadow-navbar {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  z-index: 1030;
}

.navbar-nav .nav-link {
  transition: all 0.2s ease;
  padding: 0.5rem 1rem;
  border-radius: 4px;
}

.navbar-nav .nav-link:hover {
  color: #472912;
}
</style>
