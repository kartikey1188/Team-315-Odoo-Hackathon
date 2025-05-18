<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
  <nav class="navbar">
    <div class="navbar-left">
      <h1 class="title">Title of the Project</h1>
    </div>
    <div class="navbar-links">
      <RouterLink to="/" class="nav-link">Home</RouterLink>
      <RouterLink to="/solutions" class="nav-link">Solutions</RouterLink>
      <RouterLink to="/work" class="nav-link">Work</RouterLink>
      <RouterLink to="/about" class="nav-link">About</RouterLink>
    </div>
    <div class="navbar-auth">
      <RouterLink to="/login" class="auth-btn login-btn">Login</RouterLink>
      <RouterLink to="/signup" class="auth-btn signup-btn">Sign UP</RouterLink>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  border-bottom: 1px solid #eee;
}

.navbar-left {
  display: flex;
  align-items: center;
}

.title {
  font-size: 1.2rem;
  font-weight: 600;
}

.navbar-links {
  display: flex;
  gap: 1.5rem;
}

.nav-link {
  font-weight: 500;
  padding: 0.5rem;
  transition: color 0.3s ease;
}

.nav-link:hover {
  color: #4a6cf7;
}

.navbar-auth {
  display: flex;
  gap: 1rem;
}

.auth-btn {
  padding: 0.5rem 1.5rem;
  border-radius: 4px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.login-btn {
  border: 1px solid #ddd;
}

.signup-btn {
  background-color: #4a6cf7;
  color: white;
  border: 1px solid #4a6cf7;
}

.login-btn:hover {
  background-color: #f8f9fa;
}

.signup-btn:hover {
  background-color: #3a5ce4;
}
</style> 