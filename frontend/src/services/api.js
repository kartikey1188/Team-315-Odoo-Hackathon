import axios from 'axios'

const API_URL = 'http://localhost:5000/api'

// Create axios instance with default config
const apiClient = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json'
    }
})

// Add interceptor to add auth token to requests
apiClient.interceptors.request.use(
    config => {
        const user = JSON.parse(localStorage.getItem('user') || 'null')
        if (user && user.token) {
            config.headers.Authorization = `Bearer ${user.token}`
        }
        return config
    },
    error => Promise.reject(error)
)

// Authentication services
export const authService = {
    login: async (email, password) => {
        const response = await apiClient.post('/auth/login', { email, password })
        if (response.data) {
            localStorage.setItem('user', JSON.stringify(response.data))
        }
        return response.data
    },

    register: async (name, email, password) => {
        return await apiClient.post('/auth/register', { name, email, password })
    },

    logout: () => {
        localStorage.removeItem('user')
    }
}

// User services
export const userService = {
    getCurrentUser: () => {
        return JSON.parse(localStorage.getItem('user'))
    },

    getProfile: async () => {
        return await apiClient.get('/users/profile')
    }
}

// Team services
export const teamService = {
    getTeams: async () => {
        return await apiClient.get('/teams')
    },

    createTeam: async (teamData) => {
        return await apiClient.post('/teams', teamData)
    },

    getTeamById: async (id) => {
        return await apiClient.get(`/teams/${id}`)
    }
}

// Project services
export const projectService = {
    getProjects: async () => {
        return await apiClient.get('/projects')
    },

    createProject: async (projectData) => {
        return await apiClient.post('/projects', projectData)
    },

    getProjectById: async (id) => {
        return await apiClient.get(`/projects/${id}`)
    }
}

// Task services
export const taskService = {
    getTasks: async (projectId) => {
        return await apiClient.get(`/projects/${projectId}/tasks`)
    },

    createTask: async (projectId, taskData) => {
        return await apiClient.post(`/projects/${projectId}/tasks`, taskData)
    },

    updateTaskStatus: async (taskId, status) => {
        return await apiClient.patch(`/tasks/${taskId}`, { status })
    }
} 