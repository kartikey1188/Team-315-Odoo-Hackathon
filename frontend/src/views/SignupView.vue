<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authService } from '../services/api'

const router = useRouter()
const firstName = ref('')
const lastName = ref('')
const email = ref('')
const password = ref('')
const agreeTerms = ref(false)
const error = ref('')
const isLoading = ref(false)

const handleSignup = async () => {
  try {
    if (!firstName.value || !lastName.value || !email.value || !password.value) {
      error.value = 'All fields are required'
      return
    }
    
    if (!agreeTerms.value) {
      error.value = 'You must agree to the Terms of Use and Privacy Policy'
      return
    }
    
    isLoading.value = true
    await authService.register(
      `${firstName.value} ${lastName.value}`,
      email.value,
      password.value
    )
    
    router.push('/login?registered=true')
  } catch (err) {
    error.value = err.response?.data?.message || 'Something went wrong'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="signup-container">
    <div class="signup-card">
      <h2 class="title">Create an account</h2>
      <p v-if="error" class="error-message">{{ error }}</p>
      
      <div class="login-link">
        <RouterLink to="/login">log in instead</RouterLink>
      </div>
      
      <form @submit.prevent="handleSignup">
        <div class="form-group">
          <label for="firstName">First name</label>
          <input 
            type="text" 
            id="firstName" 
            v-model="firstName" 
            class="form-control"
            :disabled="isLoading"
          />
        </div>
        
        <div class="form-group">
          <label for="lastName">Last name</label>
          <input 
            type="text" 
            id="lastName" 
            v-model="lastName" 
            class="form-control"
            :disabled="isLoading"
          />
        </div>
        
        <div class="form-group">
          <label for="email">Email</label>
          <input 
            type="email" 
            id="email" 
            v-model="email" 
            class="form-control"
            :disabled="isLoading"
          />
        </div>
        
        <div class="form-group">
          <label for="password">Password</label>
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            class="form-control"
            :disabled="isLoading"
          />
        </div>
        
        <div class="form-check">
          <input 
            type="checkbox" 
            id="terms" 
            v-model="agreeTerms" 
            class="form-check-input"
            :disabled="isLoading"
          />
          <label for="terms" class="form-check-label">
            By creating an account, I agree to our 
            <a href="#" class="terms-link">Terms of use</a> and 
            <a href="#" class="terms-link">Privacy Policy</a>
          </label>
        </div>
        
        <button type="submit" class="signup-button" :disabled="isLoading">
          {{ isLoading ? 'Creating account...' : 'Create an account' }}
        </button>
      </form>
    </div>
  </div>
</template>

<style scoped>
.signup-container {
  max-width: 600px;
  margin: 2rem auto;
  padding: 2rem;
}

.signup-card {
  background-color: #fff;
  border-radius: 8px;
  padding: 2rem;
}

.title {
  font-size: 1.75rem;
  margin-bottom: 1.5rem;
  text-align: center;
}

.login-link {
  text-align: right;
  margin-bottom: 1.5rem;
}

.login-link a {
  color: #4a6cf7;
  text-decoration: none;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-control {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.form-control:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.form-check {
  display: flex;
  align-items: flex-start;
  margin-bottom: 1.5rem;
}

.form-check-input {
  margin-right: 0.75rem;
  margin-top: 0.25rem;
}

.form-check-label {
  font-size: 0.9rem;
  line-height: 1.4;
}

.terms-link {
  color: #4a6cf7;
  text-decoration: none;
}

.signup-button {
  width: 100%;
  padding: 0.75rem;
  background-color: #4a6cf7;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.signup-button:hover:not(:disabled) {
  background-color: #3a5ce4;
}

.signup-button:disabled {
  background-color: #a5b4fc;
  cursor: not-allowed;
}

.error-message {
  background-color: #f8d7da;
  color: #721c24;
  padding: 0.75rem;
  margin-bottom: 1rem;
  border-radius: 4px;
  text-align: center;
}
</style> 