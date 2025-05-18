<template>
  <div class="work-container">
    <h1>Our Work</h1>
    <p>Explore some of our successful projects and case studies.</p>
    
    <div class="work-grid">
      <div class="work-card">
        <div class="work-image placeholder"></div>
        <h2>Project Management for Tech Startups</h2>
        <p>How we helped a growing tech startup streamline their development process.</p>
      </div>
      
      <div class="work-card">
        <div class="work-image placeholder"></div>
        <h2>Enterprise Solution for Healthcare</h2>
        <p>A comprehensive project management solution for a healthcare organization.</p>
      </div>
      
      <div class="work-card">
        <div class="work-image placeholder"></div>
        <h2>Remote Collaboration Platform</h2>
        <p>Building an effective collaboration tool for distributed teams.</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.work-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  text-align: center;
}

p {
  font-size: 1.2rem;
  color: #666;
  margin-bottom: 2rem;
  text-align: center;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
}

.work-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
  margin-top: 3rem;
}

.work-card {
  background-color: #fff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.work-card:hover {
  transform: translateY(-5px);
}

.work-image {
  height: 200px;
  width: 100%;
}

.placeholder {
  background-color: #e9ecef;
}

.work-card h2 {
  padding: 1.5rem 1.5rem 0.5rem;
  font-size: 1.5rem;
}

.work-card p {
  padding: 0 1.5rem 1.5rem;
  margin: 0;
  text-align: left;
  font-size: 1rem;
}
</style> 