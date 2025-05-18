<template>
  <div class="container">
    <div class="page-header">
      <div class="page-title">
        <router-link to="/projects" class="back-link">
          <span class="material-icons">arrow_back</span>
        </router-link>
        <h1>{{ isEditing ? 'Edit Project' : 'New Project' }}</h1>
      </div>
    </div>

    <div v-if="loading" class="loading">
      <p>Loading...</p>
    </div>
    
    <div v-else-if="error" class="error-message">
      <p>{{ error }}</p>
    </div>

    <div v-else class="form-container">
      <form @submit.prevent="saveProject">
        <div class="form-group">
          <label for="name">Project Name</label>
          <input 
            type="text" 
            id="name" 
            v-model="projectData.name" 
            required
            placeholder="Enter project name"
          >
        </div>

        <div class="form-group">
          <label for="description">Description</label>
          <textarea 
            id="description" 
            v-model="projectData.description" 
            rows="4"
            placeholder="Enter project description"
          ></textarea>
        </div>

        <div class="form-group">
          <label for="team">Team</label>
          <select id="team" v-model="projectData.team_id" required>
            <option disabled value="">Select a team</option>
            <option v-for="team in teams" :key="team.id" :value="team.id">
              {{ team.name }}
            </option>
          </select>
        </div>

        <div class="form-actions">
          <router-link to="/projects" class="btn btn-secondary">Cancel</router-link>
          <button type="submit" class="btn btn-primary" :disabled="saving">
            {{ saving ? 'Saving...' : 'Save Project' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'ProjectForm',
  props: {
    id: {
      type: [String, Number],
      required: false
    }
  },
  data() {
    return {
      isEditing: !!this.id,
      projectData: {
        name: '',
        description: '',
        team_id: ''
      },
      teams: [],
      loading: false,
      saving: false,
      error: null
    }
  },
  methods: {
    ...mapActions(['createProject', 'updateProject']),
    async loadProject() {
      if (!this.isEditing) return
      
      this.loading = true
      this.error = null
      
      try {
        // In a real app, you would fetch project data from the server
        const project = this.$store.getters.getProjects.find(p => p.id.toString() === this.id.toString())
        
        if (project) {
          this.projectData = {
            name: project.name,
            description: project.description,
            team_id: project.team_id
          }
        } else {
          this.error = 'Project not found'
        }
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to load project. Please try again.'
      } finally {
        this.loading = false
      }
    },
    async loadTeams() {
      try {
        // In a real app, you would fetch teams from the server
        // Mocking teams data for now
        this.teams = [
          { id: 1, name: 'Development Team' },
          { id: 2, name: 'Design Team' },
          { id: 3, name: 'Marketing Team' }
        ]
        
        // Set default team_id for new projects
        if (!this.isEditing && this.teams.length > 0) {
          this.projectData.team_id = this.teams[0].id
        }
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to load teams. Please try again.'
      }
    },
    async saveProject() {
      this.saving = true
      this.error = null
      
      try {
        if (this.isEditing) {
          await this.updateProject({
            id: this.id,
            projectData: this.projectData
          })
        } else {
          await this.createProject(this.projectData)
        }
        
        this.$router.push('/projects')
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to save project. Please try again.'
        this.saving = false
      }
    }
  },
  created() {
    this.loadProject()
    this.loadTeams()
  }
}
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.back-link {
  color: #4a6274;
  text-decoration: none;
  display: flex;
  align-items: center;
}

h1 {
  color: #333;
  margin: 0;
}

.form-container {
  max-width: 800px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 30px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
}

input, textarea, select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  font-family: inherit;
}

textarea {
  resize: vertical;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
  margin-top: 30px;
}

.btn {
  display: inline-block;
  padding: 10px 20px;
  background-color: #4a6274;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  border: none;
  transition: background-color 0.3s;
  font-size: 16px;
}

.btn:hover {
  background-color: #384e5f;
}

.btn-primary {
  background-color: #4a6274;
}

.btn-secondary {
  background-color: #e2e2e2;
  color: #333;
}

.btn:disabled {
  background-color: #8b9ca8;
  cursor: not-allowed;
}

.loading {
  text-align: center;
  padding: 40px 0;
}

.error-message {
  background-color: #ffebee;
  color: #c62828;
  padding: 15px;
  border-radius: 4px;
  margin-bottom: 20px;
}
</style> 