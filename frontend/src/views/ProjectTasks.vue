<template>
  <div class="container">
    <div class="page-header">
      <div class="page-title">
        <router-link to="/projects" class="back-link">
          <span class="material-icons">arrow_back</span>
        </router-link>
        <h1>{{ projectName }}</h1>
      </div>
      <router-link :to="`/projects/${projectId}/tasks/new`" class="btn btn-primary">
        <span>+ New Task</span>
      </router-link>
    </div>

    <div v-if="loading" class="loading">
      <p>Loading tasks...</p>
    </div>
    
    <div v-else-if="error" class="error-message">
      <p>{{ error }}</p>
    </div>

    <div v-else-if="tasks.length === 0" class="empty-state">
      <div class="empty-state-content">
        <h3>No tasks yet</h3>
        <p>Get started by creating your first task for this project.</p>
        <router-link :to="`/projects/${projectId}/tasks/new`" class="btn">Create Task</router-link>
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
              <div class="task-actions">
                <router-link :to="`/tasks/${task.id}/edit`" class="btn-icon">
                  <span class="material-icons">edit</span>
                </router-link>
                <button @click="confirmDelete(task)" class="btn-icon delete">
                  <span class="material-icons">delete</span>
                </button>
              </div>
            </div>
            <div class="task-card-body">
              <h3>{{ task.title }}</h3>
              <p>{{ task.description }}</p>
              <div class="task-meta">
                <span class="due-date" v-if="task.due_date">
                  <span class="material-icons">event</span>
                  {{ formatDate(task.due_date) }}
                </span>
                <span class="assignee" v-if="task.assignee_id">
                  <span class="material-icons">person</span>
                  {{ getAssigneeName(task.assignee_id) }}
                </span>
              </div>
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
              <div class="task-actions">
                <router-link :to="`/tasks/${task.id}/edit`" class="btn-icon">
                  <span class="material-icons">edit</span>
                </router-link>
                <button @click="confirmDelete(task)" class="btn-icon delete">
                  <span class="material-icons">delete</span>
                </button>
              </div>
            </div>
            <div class="task-card-body">
              <h3>{{ task.title }}</h3>
              <p>{{ task.description }}</p>
              <div class="task-meta">
                <span class="due-date" v-if="task.due_date">
                  <span class="material-icons">event</span>
                  {{ formatDate(task.due_date) }}
                </span>
                <span class="assignee" v-if="task.assignee_id">
                  <span class="material-icons">person</span>
                  {{ getAssigneeName(task.assignee_id) }}
                </span>
              </div>
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
              <div class="task-actions">
                <router-link :to="`/tasks/${task.id}/edit`" class="btn-icon">
                  <span class="material-icons">edit</span>
                </router-link>
                <button @click="confirmDelete(task)" class="btn-icon delete">
                  <span class="material-icons">delete</span>
                </button>
              </div>
            </div>
            <div class="task-card-body">
              <h3>{{ task.title }}</h3>
              <p>{{ task.description }}</p>
              <div class="task-meta">
                <span class="due-date" v-if="task.due_date">
                  <span class="material-icons">event</span>
                  {{ formatDate(task.due_date) }}
                </span>
                <span class="assignee" v-if="task.assignee_id">
                  <span class="material-icons">person</span>
                  {{ getAssigneeName(task.assignee_id) }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete confirmation modal -->
    <div v-if="showConfirmModal" class="modal">
      <div class="modal-content">
        <h3>Delete Task</h3>
        <p>Are you sure you want to delete "{{ taskToDelete?.title }}"? This action cannot be undone.</p>
        <div class="modal-actions">
          <button @click="showConfirmModal = false" class="btn btn-secondary">Cancel</button>
          <button @click="deleteTaskItem" class="btn btn-danger">Delete</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'ProjectTasks',
  props: {
    id: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      projectId: this.id,
      projectName: '',
      tasks: [],
      loading: false,
      error: null,
      showConfirmModal: false,
      taskToDelete: null
    }
  },
  computed: {
    todoTasks() {
      return this.tasks.filter(task => task.status === 'TO-DO')
    },
    inProgressTasks() {
      return this.tasks.filter(task => task.status === 'IN_PROGRESS')
    },
    doneTasks() {
      return this.tasks.filter(task => task.status === 'DONE')
    }
  },
  methods: {
    ...mapActions(['fetchProjectTasks', 'deleteTask']),
    async loadTasks() {
      this.loading = true
      this.error = null
      
      try {
        const tasks = await this.fetchProjectTasks(this.projectId)
        this.tasks = tasks
        
        // Get project name
        // This would typically come from an API call or Vuex store
        this.projectName = 'Project Details'
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
    getAssigneeName(assigneeId) {
      // In a real application, this would look up the user name from a users store
      return `User ${assigneeId}`
    },
    confirmDelete(task) {
      this.taskToDelete = task
      this.showConfirmModal = true
    },
    async deleteTaskItem() {
      if (!this.taskToDelete) return
      
      try {
        await this.deleteTask(this.taskToDelete.id)
        this.tasks = this.tasks.filter(t => t.id !== this.taskToDelete.id)
        this.showConfirmModal = false
        this.taskToDelete = null
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to delete task. Please try again.'
        this.showConfirmModal = false
      }
    }
  },
  created() {
    this.loadTasks()
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
}

.btn-primary {
  background-color: #4a6274;
}

.btn-secondary {
  background-color: #e2e2e2;
  color: #333;
}

.btn-danger {
  background-color: #d32f2f;
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
}

.task-card-header {
  padding: 10px 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #eee;
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

.task-actions {
  display: flex;
  gap: 5px;
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
}

.btn-icon:hover {
  background-color: #f5f5f5;
}

.btn-icon.delete {
  color: #d32f2f;
}

.task-card-body {
  padding: 15px;
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

.task-meta {
  display: flex;
  align-items: center;
  gap: 15px;
  font-size: 0.8rem;
  color: #666;
}

.due-date, .assignee {
  display: flex;
  align-items: center;
  gap: 5px;
}

.material-icons {
  font-size: 1rem;
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

/* Media query for desktop */
@media (max-width: 1200px) {
  .task-columns {
    grid-template-columns: 1fr;
  }
}
</style> 