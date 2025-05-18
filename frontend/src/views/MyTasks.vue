<template>
  <div class="container">
    <div class="page-header">
      <h1>My Tasks</h1>
    </div>

    <div v-if="loading" class="loading">
      <p>Loading your tasks...</p>
    </div>
    
    <div v-else-if="error" class="error-message">
      <p>{{ error }}</p>
    </div>

    <div v-else-if="myTasks.length === 0" class="empty-state">
      <div class="empty-state-content">
        <h3>No tasks assigned to you</h3>
        <p>You don't have any tasks assigned to you yet.</p>
        <router-link to="/projects" class="btn">View Projects</router-link>
      </div>
    </div>

    <div v-else class="task-columns">
      <div class="task-column">
        <div class="column-header">
          <h2>To Do</h2>
        </div>
        <div class="task-list">
          <div 
            v-for="task in todoTasks" 
            :key="task.id" 
            class="task-card"
          >
            <div class="task-card-header">
              <span class="task-status todo">TO-DO</span>
              <span class="project-name">{{ getProjectName(task.project_id) }}</span>
            </div>
            <div class="task-card-body">
              <h3>{{ task.title }}</h3>
              <p>{{ task.description }}</p>
              <div class="task-meta">
                <span class="due-date" v-if="task.due_date">
                  <span class="material-icons">event</span>
                  {{ formatDate(task.due_date) }}
                </span>
              </div>
            </div>
            <div class="task-card-footer">
              <button @click="updateTaskStatus(task, 'IN_PROGRESS')" class="btn btn-primary">
                Start
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="task-column">
        <div class="column-header">
          <h2>In Progress</h2>
        </div>
        <div class="task-list">
          <div 
            v-for="task in inProgressTasks" 
            :key="task.id" 
            class="task-card"
          >
            <div class="task-card-header">
              <span class="task-status in-progress">IN PROGRESS</span>
              <span class="project-name">{{ getProjectName(task.project_id) }}</span>
            </div>
            <div class="task-card-body">
              <h3>{{ task.title }}</h3>
              <p>{{ task.description }}</p>
              <div class="task-meta">
                <span class="due-date" v-if="task.due_date">
                  <span class="material-icons">event</span>
                  {{ formatDate(task.due_date) }}
                </span>
              </div>
            </div>
            <div class="task-card-footer">
              <button @click="updateTaskStatus(task, 'DONE')" class="btn btn-success">
                Complete
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="task-column">
        <div class="column-header">
          <h2>Done</h2>
        </div>
        <div class="task-list">
          <div 
            v-for="task in doneTasks" 
            :key="task.id" 
            class="task-card"
          >
            <div class="task-card-header">
              <span class="task-status done">DONE</span>
              <span class="project-name">{{ getProjectName(task.project_id) }}</span>
            </div>
            <div class="task-card-body">
              <h3>{{ task.title }}</h3>
              <p>{{ task.description }}</p>
              <div class="task-meta">
                <span class="due-date" v-if="task.due_date">
                  <span class="material-icons">event</span>
                  {{ formatDate(task.due_date) }}
                </span>
                <span class="completed-date">
                  <span class="material-icons">check_circle</span>
                  Completed
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'MyTasks',
  data() {
    return {
      loading: false,
      error: null
    }
  },
  computed: {
    ...mapGetters(['getMyTasks']),
    myTasks() {
      return this.getMyTasks
    },
    todoTasks() {
      return this.myTasks.filter(task => task.status === 'TO-DO')
    },
    inProgressTasks() {
      return this.myTasks.filter(task => task.status === 'IN_PROGRESS')
    },
    doneTasks() {
      return this.myTasks.filter(task => task.status === 'DONE')
    }
  },
  methods: {
    ...mapActions(['fetchProjectTasks', 'updateTask']),
    async loadAllTasks() {
      this.loading = true
      this.error = null
      
      try {
        // In a real app, you would have an API endpoint to get all tasks for the current user
        // Here we're fetching all project tasks and filtering them in the store
        
        // This is just a placeholder. In a real app, you would have a dedicated API endpoint
        // and store action to fetch all tasks assigned to the current user across all projects
        const projects = this.$store.getters.getProjects
        
        for (const project of projects) {
          await this.fetchProjectTasks(project.id)
        }
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to load tasks. Please try again.'
      } finally {
        this.loading = false
      }
    },
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString()
    },
    getProjectName(projectId) {
      const project = this.$store.getters.getProjects.find(p => p.id === projectId)
      return project ? project.name : `Project ${projectId}`
    },
    async updateTaskStatus(task, newStatus) {
      try {
        await this.updateTask({
          id: task.id,
          taskData: {
            ...task,
            status: newStatus
          }
        })
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to update task status. Please try again.'
      }
    }
  },
  created() {
    this.loadAllTasks()
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

.task-columns {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.task-column {
  background-color: #f5f7f9;
  border-radius: 8px;
  padding: 15px;
}

.column-header {
  margin-bottom: 15px;
}

.column-header h2 {
  font-size: 1.2rem;
  color: #4a6274;
  margin: 0;
}

.task-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
  min-height: 200px;
}

.task-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.task-card-header {
  padding: 10px 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #eee;
}

.project-name {
  font-size: 0.8rem;
  color: #666;
}

.task-status {
  font-size: 0.8rem;
  font-weight: 500;
  padding: 4px 8px;
  border-radius: 4px;
}

.task-status.todo {
  background-color: #e3f2fd;
  color: #1976d2;
}

.task-status.in-progress {
  background-color: #fff8e1;
  color: #ff8f00;
}

.task-status.done {
  background-color: #e8f5e9;
  color: #388e3c;
}

.task-card-body {
  padding: 15px;
  flex-grow: 1;
}

.task-card-body h3 {
  margin-top: 0;
  margin-bottom: 10px;
  font-size: 1rem;
  color: #333;
}

.task-card-body p {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 15px;
}

.task-card-footer {
  padding: 15px;
  border-top: 1px solid #eee;
}

.task-meta {
  display: flex;
  align-items: center;
  gap: 15px;
  font-size: 0.8rem;
  color: #666;
}

.due-date, .completed-date {
  display: flex;
  align-items: center;
  gap: 5px;
}

.completed-date {
  color: #388e3c;
}

.material-icons {
  font-size: 1rem;
}

.btn {
  display: inline-block;
  padding: 8px 12px;
  background-color: #4a6274;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  border: none;
  transition: background-color 0.3s;
  font-size: 0.9rem;
  width: 100%;
  text-align: center;
}

.btn-primary {
  background-color: #4a6274;
}

.btn-success {
  background-color: #388e3c;
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

/* Media query for desktop */
@media (max-width: 1200px) {
  .task-columns {
    grid-template-columns: 1fr;
  }
}
</style> 