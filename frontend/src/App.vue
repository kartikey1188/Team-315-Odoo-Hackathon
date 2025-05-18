<template>
  <div id="app">
    <nav v-if="$route.meta.requiresAuth">
      <div class="nav-container">
        <div class="logo">SynergySphere</div>
        <div class="nav-links">
          <router-link to="/projects">Projects</router-link>
          <router-link to="/my-tasks">My Tasks</router-link>
          <a href="#" @click.prevent="logout">Logout</a>
        </div>
      </div>
    </nav>
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App',
  methods: {
    logout() {
      // Clear any stored authentication
      localStorage.removeItem('user');
      // Redirect to login page
      this.$router.push('/login');
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Arial', sans-serif;
  background-color: #f5f5f5;
  color: #333;
}

#app {
  min-height: 100vh;
}

nav {
  background-color: #4a6274;
  padding: 15px 0;
  color: white;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
}

.nav-links {
  display: flex;
  gap: 20px;
}

.nav-links a {
  color: white;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s;
}

.nav-links a:hover {
  color: #afd3e2;
}

.router-link-active {
  color: #afd3e2 !important;
  border-bottom: 2px solid #afd3e2;
  padding-bottom: 3px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}
</style> 