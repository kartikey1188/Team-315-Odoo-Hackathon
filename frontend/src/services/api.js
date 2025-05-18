import axios from 'axios'

const API_URL = 'http://localhost:5000/api'

// Set default base URL and headers
axios.defaults.baseURL = API_URL
axios.defaults.headers.common['Content-Type'] = 'application/json'
axios.defaults.withCredentials = true

// Create API service object
const apiService = {
    // Auth
    login(credentials) {
        return axios.post('/login', credentials)
    },
    register(userData) {
        return axios.post('/register', userData)
    },

    // Projects
    getProjects() {
        return axios.get('/projects')
    },
    getProject(id) {
        return axios.get(`/projects/${id}`)
    },
    createProject(project) {
        return axios.post('/projects', project)
    },
    updateProject(id, project) {
        return axios.put(`/projects/${id}`, project)
    },
    deleteProject(id) {
        return axios.delete(`/projects/${id}`)
    },

    // Tasks
    getProjectTasks(projectId) {
        return axios.get(`/projects/${projectId}/tasks`)
    },
    getTask(id) {
        return axios.get(`/tasks/${id}`)
    },
    createTask(projectId, task) {
        return axios.post(`/projects/${projectId}/tasks`, task)
    },
    updateTask(id, task) {
        return axios.put(`/tasks/${id}`, task)
    },
    deleteTask(id) {
        return axios.delete(`/tasks/${id}`)
    },

    // Teams
    getTeams() {
        return axios.get('/teams')
    },
    getTeam(id) {
        return axios.get(`/teams/${id}`)
    },
    getTeamMembers(teamId) {
        return axios.get(`/teams/${teamId}/members`)
    }
}

export default apiService 