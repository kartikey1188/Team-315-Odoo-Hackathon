<template>
  <div class="solutions-container">
    <h1>Our Solutions</h1>
    <p>Discover how our platform can solve your project management challenges.</p>
    
    <div class="solutions-grid">
      <div class="solution-card">
        <h2>For Small Teams</h2>
        <p>Perfect for startups and small teams looking to organize their workflow efficiently.</p>
      </div>
      
      <div class="solution-card">
        <h2>For Enterprise</h2>
        <p>Scalable solutions for large organizations with complex project requirements.</p>
      </div>
      
      <div class="solution-card">
        <h2>For Remote Teams</h2>
        <p>Tools designed specifically for distributed teams to collaborate effectively.</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.solutions-container {
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

.solutions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 3rem;
}

.solution-card {
  background-color: #f8f9fa;
  padding: 2rem;
  border-radius: 8px;
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.solution-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.solution-card h2 {
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

.solution-card p {
  color: #666;
  font-size: 1rem;
}
</style> 