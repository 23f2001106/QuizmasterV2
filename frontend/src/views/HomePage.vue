<template>
  <div class="homepage d-flex flex-column min-vh-100 justify-content-between">
    <NavBar />
    <HomeSection />
    <AboutSection />
    <FeatureSection />
    <ContactSection />
    <AppFooter />
  </div>
</template>

<script>
import NavBar from "@/components/NavBar.vue";
import AppFooter from "@/components/AppFooter.vue";
import HomeSection from "@/components/HomePage/HomeSection.vue";
import AboutSection from "@/components/HomePage/AboutSection.vue";
import FeatureSection from "@/components/HomePage/FeatureSection.vue";
import ContactSection from "@/components/HomePage/ContactSection.vue";

export default {
  name: "HomePage",
  components: {
    NavBar,
    AppFooter,
    HomeSection,
    AboutSection,
    FeatureSection,
    ContactSection,
  },
  mounted() {
    // Scroll to section if query param exists
    const section = this.$route.query.scrollTo;
    if (section) {
      this.$nextTick(() => {
        const el = document.getElementById(section);
        if (el) {
          el.scrollIntoView({ behavior: "smooth" });
        }
      });
    }
  },
};
</script>

<style scoped>
.homepage {
  background-color: #ffffff;
}
</style>
