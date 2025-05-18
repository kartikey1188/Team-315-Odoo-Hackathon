<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const user = ref(null)

onMounted(() => {
  const storedUser = localStorage.getItem('user')
  if (storedUser) {
    user.value = JSON.parse(storedUser)
  }
})
</script>

<template>
  <div class="home-container">
    <div class="hero-section">
      <h1>Welcome to Our Project Management Platform</h1>
      <p>Streamline your team collaboration and project management with our powerful tools</p>
      
      <div class="cta-buttons">
        <RouterLink v-if="!user" to="/signup" class="cta-button primary">Get Started</RouterLink>
        <RouterLink v-if="!user" to="/login" class="cta-button secondary">Login</RouterLink>
        <RouterLink v-if="user" to="/projects" class="cta-button primary">View Projects</RouterLink>
      </div>
    </div>
    
    <div class="features-section">
      <h2>Key Features</h2>
      
      <div class="features-grid">
        <div class="feature-card">
          <h3>Team Collaboration</h3>
          <p>Work together seamlessly with your team members on various projects</p>
        </div>
        
        <div class="feature-card">
          <h3>Task Management</h3>
          <p>Organize and track tasks efficiently with our intuitive task management system</p>
        </div>
        
        <div class="feature-card">
          <h3>Project Tracking</h3>
          <p>Monitor project progress and deadlines with comprehensive tracking tools</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.hero-section {
  text-align: center;
  padding: 4rem 2rem;
}

.hero-section h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.hero-section p {
  font-size: 1.2rem;
  color: #666;
  margin-bottom: 2rem;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
}

.cta-buttons {
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.cta-button {
  padding: 0.75rem 2rem;
  border-radius: 4px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
}

.primary {
  background-color: #4a6cf7;
  color: white;
}

.secondary {
  background-color: transparent;
  color: #4a6cf7;
  border: 1px solid #4a6cf7;
}

.primary:hover {
  background-color: #3a5ce4;
}

.secondary:hover {
  background-color: rgba(74, 108, 247, 0.1);
}

.features-section {
  padding: 4rem 2rem;
}

.features-section h2 {
  text-align: center;
  margin-bottom: 3rem;
  font-size: 2rem;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.feature-card {
  background-color: #f8f9fa;
  padding: 2rem;
  border-radius: 8px;
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.feature-card h3 {
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

.feature-card p {
  color: #666;
}

@media (max-width: 768px) {
  .hero-section h1 {
    font-size: 2rem;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
  }
}
</style> 