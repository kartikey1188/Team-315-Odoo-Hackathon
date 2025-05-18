<template>
  <div class="about-container">
    <div class="about-header">
      <h1>About Us</h1>
      <p>Learn more about our mission and the team behind the platform.</p>
    </div>
    
    <div class="about-section">
      <h2>Our Mission</h2>
      <p>
        We aim to provide the most intuitive and efficient project management tools for teams of all sizes.
        Our platform is designed to simplify collaboration and help teams achieve their goals faster.
      </p>
    </div>
    
    <div class="about-section">
      <h2>Our Story</h2>
      <p>
        Founded in 2023, our company started with a simple idea: to create a better way for teams to work together.
        We've since grown into a platform that serves teams around the world, helping them organize their work and
        collaborate more effectively.
      </p>
    </div>
    
    <div class="about-section">
      <h2>Our Team</h2>
      <div class="team-grid">
        <div class="team-member">
          <div class="team-photo placeholder"></div>
          <h3>John Doe</h3>
          <p>Co-founder & CEO</p>
        </div>
        
        <div class="team-member">
          <div class="team-photo placeholder"></div>
          <h3>Jane Smith</h3>
          <p>Co-founder & CTO</p>
        </div>
        
        <div class="team-member">
          <div class="team-photo placeholder"></div>
          <h3>Mike Johnson</h3>
          <p>Head of Product</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.about-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.about-header {
  text-align: center;
  margin-bottom: 3rem;
}

.about-header h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.about-header p {
  font-size: 1.2rem;
  color: #666;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
}

.about-section {
  margin-bottom: 4rem;
}

.about-section h2 {
  font-size: 1.8rem;
  margin-bottom: 1.5rem;
  position: relative;
  padding-bottom: 0.5rem;
}

.about-section h2:after {
  content: "";
  position: absolute;
  left: 0;
  bottom: 0;
  width: 50px;
  height: 3px;
  background-color: #4a6cf7;
}

.about-section p {
  font-size: 1.1rem;
  color: #555;
  line-height: 1.7;
  max-width: 800px;
}

.team-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.team-member {
  text-align: center;
}

.team-photo {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  margin: 0 auto 1rem;
}

.placeholder {
  background-color: #e9ecef;
}

.team-member h3 {
  font-size: 1.3rem;
  margin-bottom: 0.5rem;
}

.team-member p {
  color: #666;
  font-size: 1rem;
}

@media (max-width: 768px) {
  .about-section h2 {
    font-size: 1.5rem;
  }
  
  .team-grid {
    grid-template-columns: 1fr;
  }
}
</style> 