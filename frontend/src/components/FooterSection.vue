<script setup>
// Footer component
</script>

<template>
  <footer class="footer">
    <div class="footer-container">
      <div class="footer-left">
        <div class="company-banner">
          <h3>Company's Banner</h3>
        </div>
      </div>
      
      <div class="footer-links">
        <div class="footer-column">
          <h4>Quick Links</h4>
          <ul>
            <li><a href="#">Link 1</a></li>
            <li><a href="#">Link 2</a></li>
            <li><a href="#">Link 3</a></li>
            <li><a href="#">Link 4</a></li>
          </ul>
        </div>
        
        <div class="footer-column">
          <h4>Company</h4>
          <ul>
            <li><a href="#">About Us</a></li>
            <li><a href="#">Careers</a></li>
            <li><a href="#">Services</a></li>
            <li><a href="#">Contact</a></li>
          </ul>
        </div>
        
        <div class="footer-column">
          <h4>Connect with us</h4>
          <div class="social-links">
            <a href="#" class="social-link">Facebook</a>
            <a href="#" class="social-link">Twitter</a>
            <a href="#" class="social-link">LinkedIn</a>
            <a href="#" class="social-link">Instagram</a>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  background-color: #f8f9fa;
  padding: 3rem 2rem;
  border-top: 1px solid #eee;
}

.footer-container {
  display: flex;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
}

.footer-left {
  flex: 1;
}

.company-banner {
  border: 1px solid #ddd;
  padding: 2rem;
  border-radius: 8px;
  height: 150px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.footer-links {
  flex: 2;
  display: flex;
  justify-content: space-around;
}

.footer-column h4 {
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

.footer-column ul {
  list-style: none;
}

.footer-column ul li {
  margin-bottom: 0.5rem;
}

.footer-column ul li a {
  color: #555;
  transition: color 0.3s ease;
}

.footer-column ul li a:hover {
  color: #4a6cf7;
}

.social-links {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.social-link {
  color: #555;
  transition: color 0.3s ease;
}

.social-link:hover {
  color: #4a6cf7;
}

@media (max-width: 768px) {
  .footer-container {
    flex-direction: column;
    gap: 2rem;
  }
  
  .footer-links {
    flex-direction: column;
    gap: 1.5rem;
  }
}
</style> 