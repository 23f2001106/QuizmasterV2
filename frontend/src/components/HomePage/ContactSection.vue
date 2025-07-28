<template>
  <section id="contact" class="contact-section d-flex">
    <!-- Left Side: Message -->
    <div class="contact-right d-flex align-items-center justify-content-center">
      <form class="contact-form" @submit.prevent="handleSubmit">
        <div class="form-group">
          <input
            type="text"
            placeholder="Full Name"
            v-model="contactForm.name"
            required
          />
        </div>
        <div class="form-group">
          <input
            type="email"
            placeholder="Email Address"
            v-model="contactForm.email"
            required
          />
        </div>
        <div class="form-group">
          <textarea
            placeholder="Your Message"
            rows="5"
            v-model="contactForm.message"
            required
          ></textarea>
        </div>
        <button type="submit" class="btn btn-submit">Send Message</button>
      </form>
    </div>

    <!-- Right Side: Contact Form -->
    <div class="contact-left d-flex align-items-center justify-content-center">
      <div class="contact-message text-center">
        <h2 class="contact-title">Get in Touch</h2>
        <p class="contact-text">
          We'd love to hear from you! Whether you have questions, feedback, or
          just want to say hello — drop us a message and we'll get back to you
          shortly.
        </p>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: "ContactSection",
  data() {
    return {
      contactForm: {
        name: "",
        email: "",
        message: "",
      },
    };
  },
  methods: {
    handleSubmit() {
      if (
        this.contactForm.name &&
        this.contactForm.email &&
        this.contactForm.message
      ) {
        alert(`Thanks, ${this.contactForm.name}! We've received your message.`);
        this.contactForm.name = "";
        this.contactForm.email = "";
        this.contactForm.message = "";
      } else {
        alert("Please fill in all fields before submitting.");
      }
    },
  },
};
</script>

<style scoped>
.contact-section {
  background-color: #faece0;
  display: flex;
  flex-direction: row;
  padding: 60px 0;
}

.contact-left,
.contact-right {
  flex: 1;
  padding: 40px;
}

.contact-message {
  max-width: 500px;
}

.contact-title {
  font-size: 2rem;
  font-weight: bold;
  text-transform: uppercase;
  color: #5c4033;
  margin-bottom: 20px;
  position: relative;
}

.contact-title::after {
  content: "";
  display: block;
  width: 60px;
  height: 2px;
  background-color: #a97449;
  margin: 8px auto 0;
}

.contact-title:hover {
  transform: scale(1.05);
  transition: all 0.3s ease;
}

.contact-text {
  font-size: 1.1rem;
  color: #333;
  line-height: 1.6;
}

.contact-form {
  width: 100%;
  max-width: 500px;
  background-color: #fff;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 20px;
}

.contact-form input,
.contact-form textarea {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1rem;
  font-family: inherit;
  outline: none;
  transition: border-color 0.3s;
}

.contact-form input:focus,
.contact-form textarea:focus {
  border-color: #a97449;
}

.btn-submit {
  background-color: #5c4033;
  color: #fff;
  padding: 12px 25px;
  border: 1px solid transparent;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-submit:hover {
  background-color: transparent;
  color: #5c4033;
  border: 1px solid #5c4033;
  transition: all 0.3s ease;
}
</style>
