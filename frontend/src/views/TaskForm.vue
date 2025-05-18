<template>
  <div class="container">
    <div class="page-header">
      <div class="page-title">
        <router-link :to="isEditing ? `/projects/${task.project_id}/tasks` : `/projects/${projectId}/tasks`" class="back-link">
          <span class="material-icons">arrow_back</span>
        </router-link>
        <h1>{{ isEditing ? 'Edit Task' : 'New Task' }}</h1>
      </div>
    </div>

    <div v-if="loading" class="loading">
      <p>Loading...</p>
    </div>
    
    <div v-else-if="error" class="error-message">
      <p>{{ error }}</p>
    </div>

    <div v-else class="form-container">
      <form @submit.prevent="saveTask">
        <div class="form-group">
          <label for="title">Task Title</label>
          <input 
            type="text" 
            id="title" 
            v-model="task.title" 
            required
            placeholder="Enter task title"
          >
        </div>

        <div class="form-group">
          <label for="description">Description</label>
          <textarea 
            id="description" 
            v-model="task.description" 
            rows="4"
            placeholder="Enter task description"
          ></textarea>
        </div>

        <div class="form-group">
          <label for="status">Status</label>
          <select id="status" v-model="task.status" required>
            <option value="TO-DO">To Do</option>
            <option value="IN_PROGRESS">In Progress</option>
            <option value="DONE">Done</option>
          </select>
        </div>

        <div class="form-group">
          <label for="due_date">Due Date</label>
          <input 
            type="date" 
            id="due_date" 
            v-model="task.due_date"
          >
        </div>

        <div class="form-group">
          <label for="assignee">Assignee</label>
          <select id="assignee" v-model="task.assignee_id">
            <option value="">Unassigned</option>
            <option v-for="user in users" :key="user.id" :value="user.id">
              {{ user.name }}
            </option>
          </select>
        </div>

        <div class="form-actions">
          <router-link :to="isEditing ? `/projects/${task.project_id}/tasks` : `/projects/${projectId}/tasks`" class="btn btn-secondary">Cancel</router-link>
          <button type="submit" class="btn btn-primary" :disabled="saving">
            {{ saving ? 'Saving...' : 'Save Task' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'TaskForm',
  props: {
    id: {
      type: [String, Number],
      required: false
    },
    projectId: {
      type: [String, Number],
      required: false
    }
  },
  data() {
    return {
      isEditing: !!this.id,
      task: {
        title: '',
        description: '',
        status: 'TO-DO',
        due_date: '',
        project_id: this.projectId || '',
        assignee_id: ''
      },
      users: [],
      loading: false,
      saving: false,
      error: null
    }
  },
  methods: {
    ...mapActions(['createTask', 'updateTask']),
    async loadTask() {
      if (!this.isEditing) return
      
      this.loading = true
      this.error = null
      
      try {
        // In a real app, you would fetch task data from an API
        // For now, we'll simulate by finding it in the store
        const allTasks = []
        const projects = this.$store.getters.getProjects
        
        for (const project of projects) {
          const projectTasks = await this.fetchProjectTasks(project.id)
          allTasks.push(...projectTasks)
        }
        
        const task = allTasks.find(t => t.id.toString() === this.id.toString())
        
        if (task) {
          this.task = {
            title: task.title,
            description: task.description,
            status: task.status,
            due_date: task.due_date ? task.due_date.substring(0, 10) : '', // Format for date input
            project_id: task.project_id,
            assignee_id: task.assignee_id
          }
        } else {
          this.error = 'Task not found'
        }
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to load task. Please try again.'
      } finally {
        this.loading = false
      }
    },
    async loadUsers() {
      try {
        // In a real app, you would fetch users from the server
        // Mocking users data for now
        this.users = [
          { id: 1, name: 'John Doe' },
          { id: 2, name: 'Jane Smith' },
          { id: 3, name: 'Bob Johnson' }
        ]
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to load users. Please try again.'
      }
    },
    async saveTask() {
      this.saving = true
      this.error = null
      
      try {
        if (this.isEditing) {
          await this.updateTask({
            id: this.id,
            taskData: this.task
          })
          this.$router.push(`/projects/${this.task.project_id}/tasks`)
        } else {
          await this.createTask({
            projectId: this.projectId,
            taskData: this.task
          })
          this.$router.push(`/projects/${this.projectId}/tasks`)
        }
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to save task. Please try again.'
        this.saving = false
      }
    }
  },
  created() {
    this.loadTask()
    this.loadUsers()
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