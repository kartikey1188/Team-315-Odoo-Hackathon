<template>
  <div class="container">
    <div class="page-header">
      <h1>Projects</h1>
      <router-link to="/projects/new" class="btn btn-primary">
        <span>+ New Project</span>
      </router-link>
    </div>

    <div v-if="loading" class="loading">
      <p>Loading projects...</p>
    </div>
    
    <div v-else-if="error" class="error-message">
      <p>{{ error }}</p>
    </div>

    <div v-else-if="projects.length === 0" class="empty-state">
      <div class="empty-state-content">
        <h3>No projects yet</h3>
        <p>Get started by creating your first project.</p>
        <router-link to="/projects/new" class="btn">Create Project</router-link>
      </div>
    </div>

    <div v-else class="project-grid">
      <div v-for="project in projects" :key="project.id" class="project-card">
        <div class="project-card-body">
          <h3>{{ project.name }}</h3>
          <p>{{ project.description }}</p>
        </div>
        <div class="project-card-footer">
          <router-link :to="`/projects/${project.id}/tasks`" class="btn btn-view">View Tasks</router-link>
          <div class="actions">
            <router-link :to="`/projects/${project.id}/edit`" class="btn-icon">
              <span class="material-icons">edit</span>
            </router-link>
            <button @click="confirmDelete(project)" class="btn-icon delete">
              <span class="material-icons">delete</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete confirmation modal -->
    <div v-if="showConfirmModal" class="modal">
      <div class="modal-content">
        <h3>Delete Project</h3>
        <p>Are you sure you want to delete "{{ projectToDelete?.name }}"? This action cannot be undone.</p>
        <div class="modal-actions">
          <button @click="showConfirmModal = false" class="btn btn-secondary">Cancel</button>
          <button @click="deleteProject" class="btn btn-danger">Delete</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'Projects',
  data() {
    return {
      loading: false,
      error: null,
      showConfirmModal: false,
      projectToDelete: null
    }
  },
  computed: {
    ...mapGetters(['getProjects']),
    projects() {
      return this.getProjects
    }
  },
  methods: {
    ...mapActions(['fetchProjects', 'deleteProject']),
    async loadProjects() {
      this.loading = true
      this.error = null
      
      try {
        await this.fetchProjects()
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to load projects. Please try again.'
      } finally {
        this.loading = false
      }
    },
    confirmDelete(project) {
      this.projectToDelete = project
      this.showConfirmModal = true
    },
    async deleteProjectItem() {
      if (!this.projectToDelete) return
      
      try {
        await this.deleteProject(this.projectToDelete.id)
        this.showConfirmModal = false
        this.projectToDelete = null
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to delete project. Please try again.'
        this.showConfirmModal = false
      }
    }
  },
  created() {
    this.loadProjects()
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

h1 {
  color: #333;
  margin: 0;
}

.btn {
  display: inline-block;
  padding: 10px 15px;
  background-color: #4a6274;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  border: none;
  transition: background-color 0.3s;
}

.btn:hover {
  background-color: #384e5f;
}

.btn-primary {
  background-color: #4a6274;
  padding: 10px 15px;
}

.btn-secondary {
  background-color: #e2e2e2;
  color: #333;
}

.btn-danger {
  background-color: #d32f2f;
}

.btn-view {
  width: 100%;
  text-align: center;
  background-color: #4a6274;
}

.project-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.project-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: transform 0.3s, box-shadow 0.3s;
}

.project-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.project-card-body {
  padding: 20px;
  flex-grow: 1;
}

.project-card-body h3 {
  color: #333;
  margin-top: 0;
  margin-bottom: 10px;
}

.project-card-body p {
  color: #666;
  margin-bottom: 0;
}

.project-card-footer {
  padding: 15px;
  border-top: 1px solid #eee;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 10px;
}

.btn-icon {
  background: none;
  border: none;
  color: #4a6274;
  cursor: pointer;
  text-decoration: none;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 5px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.btn-icon:hover {
  background-color: #f5f5f5;
}

.btn-icon.delete {
  color: #d32f2f;
}

.loading, .empty-state {
  text-align: center;
  padding: 40px 0;
}

.empty-state-content {
  max-width: 400px;
  margin: 0 auto;
  padding: 40px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.empty-state-content h3 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #333;
}

.empty-state-content p {
  color: #666;
  margin-bottom: 20px;
}

.error-message {
  background-color: #ffebee;
  color: #c62828;
  padding: 15px;
  border-radius: 4px;
  margin-bottom: 20px;
}

/* Modal styles */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  border-radius: 8px;
  padding: 25px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.modal-content h3 {
  margin-top: 0;
  color: #333;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

/* Add material icons via CDN */
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');
</style> 