import { createStore } from 'vuex'
import axios from 'axios'

// API Base URL
const API_URL = 'http://localhost:5000/api'

export default createStore({
    state: {
        user: JSON.parse(localStorage.getItem('user')) || null,
        projects: [],
        tasks: [],
        teams: []
    },
    getters: {
        isAuthenticated: state => !!state.user,
        getUserId: state => state.user ? state.user.id : null,
        getProjects: state => state.projects,
        getTasks: state => state.tasks,
        getMyTasks: state => {
            if (!state.user) return []
            return state.tasks.filter(task => task.assignee_id === state.user.id)
        }
    },
    mutations: {
        setUser(state, user) {
            state.user = user
            localStorage.setItem('user', JSON.stringify(user))
        },
        clearUser(state) {
            state.user = null
            localStorage.removeItem('user')
        },
        setProjects(state, projects) {
            state.projects = projects
        },
        setTasks(state, tasks) {
            state.tasks = tasks
        },
        addProject(state, project) {
            state.projects.push(project)
        },
        updateProject(state, updatedProject) {
            const index = state.projects.findIndex(p => p.id === updatedProject.id)
            if (index !== -1) {
                state.projects.splice(index, 1, updatedProject)
            }
        },
        deleteProject(state, projectId) {
            state.projects = state.projects.filter(p => p.id !== projectId)
        },
        addTask(state, task) {
            state.tasks.push(task)
        },
        updateTask(state, updatedTask) {
            const index = state.tasks.findIndex(t => t.id === updatedTask.id)
            if (index !== -1) {
                state.tasks.splice(index, 1, updatedTask)
            }
        },
        deleteTask(state, taskId) {
            state.tasks = state.tasks.filter(t => t.id !== taskId)
        }
    },
    actions: {
        // Auth actions
        async register({ commit }, userData) {
            try {
                const response = await axios.post(`${API_URL}/register`, userData)
                return response
            } catch (error) {
                throw error
            }
        },
        async login({ commit }, credentials) {
            try {
                const response = await axios.post(`${API_URL}/login`, credentials)
                if (response.status === 200) {
                    // In a real app, you'd get user data from the response
                    // Using mockup user data here
                    const user = {
                        id: 1, // This would come from the server
                        email: credentials.email,
                        name: 'User Name' // This would come from the server
                    }
                    commit('setUser', user)
                    return user
                }
            } catch (error) {
                throw error
            }
        },
        logout({ commit }) {
            commit('clearUser')
        },

        // Project actions
        async fetchProjects({ commit }) {
            try {
                const response = await axios.get(`${API_URL}/projects`)
                commit('setProjects', response.data)
                return response.data
            } catch (error) {
                throw error
            }
        },
        async createProject({ commit }, projectData) {
            try {
                const response = await axios.post(`${API_URL}/projects`, projectData)
                commit('addProject', response.data)
                return response.data
            } catch (error) {
                throw error
            }
        },
        async updateProject({ commit }, { id, projectData }) {
            try {
                const response = await axios.put(`${API_URL}/projects/${id}`, projectData)
                commit('updateProject', response.data)
                return response.data
            } catch (error) {
                throw error
            }
        },
        async deleteProject({ commit }, id) {
            try {
                await axios.delete(`${API_URL}/projects/${id}`)
                commit('deleteProject', id)
            } catch (error) {
                throw error
            }
        },

        // Task actions
        async fetchProjectTasks({ commit }, projectId) {
            try {
                const response = await axios.get(`${API_URL}/projects/${projectId}/tasks`)
                commit('setTasks', response.data)
                return response.data
            } catch (error) {
                throw error
            }
        },
        async createTask({ commit }, { projectId, taskData }) {
            try {
                const response = await axios.post(`${API_URL}/projects/${projectId}/tasks`, taskData)
                commit('addTask', response.data)
                return response.data
            } catch (error) {
                throw error
            }
        },
        async updateTask({ commit }, { id, taskData }) {
            try {
                const response = await axios.put(`${API_URL}/tasks/${id}`, taskData)
                commit('updateTask', response.data)
                return response.data
            } catch (error) {
                throw error
            }
        },
        async deleteTask({ commit }, id) {
            try {
                await axios.delete(`${API_URL}/tasks/${id}`)
                commit('deleteTask', id)
            } catch (error) {
                throw error
            }
        }
    }
}) 