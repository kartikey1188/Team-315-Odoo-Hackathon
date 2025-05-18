import { createRouter, createWebHistory } from 'vue-router'

// Views
import Login from '../views/Login.vue'
import SignUp from '../views/SignUp.vue'
import Projects from '../views/Projects.vue'
import ProjectTasks from '../views/ProjectTasks.vue'
import MyTasks from '../views/MyTasks.vue'
import ProjectForm from '../views/ProjectForm.vue'
import TaskForm from '../views/TaskForm.vue'

// Auth guard
const requireAuth = (to, from, next) => {
    const user = JSON.parse(localStorage.getItem('user'))
    if (!user) {
        next('/login')
    } else {
        next()
    }
}

const routes = [
    {
        path: '/',
        redirect: '/login'
    },
    {
        path: '/login',
        name: 'Login',
        component: Login,
        meta: { requiresAuth: false }
    },
    {
        path: '/signup',
        name: 'SignUp',
        component: SignUp,
        meta: { requiresAuth: false }
    },
    {
        path: '/projects',
        name: 'Projects',
        component: Projects,
        meta: { requiresAuth: true },
        beforeEnter: requireAuth
    },
    {
        path: '/projects/:id/tasks',
        name: 'ProjectTasks',
        component: ProjectTasks,
        meta: { requiresAuth: true },
        beforeEnter: requireAuth,
        props: true
    },
    {
        path: '/my-tasks',
        name: 'MyTasks',
        component: MyTasks,
        meta: { requiresAuth: true },
        beforeEnter: requireAuth
    },
    {
        path: '/projects/new',
        name: 'NewProject',
        component: ProjectForm,
        meta: { requiresAuth: true },
        beforeEnter: requireAuth
    },
    {
        path: '/projects/:id/edit',
        name: 'EditProject',
        component: ProjectForm,
        meta: { requiresAuth: true },
        beforeEnter: requireAuth,
        props: true
    },
    {
        path: '/projects/:projectId/tasks/new',
        name: 'NewTask',
        component: TaskForm,
        meta: { requiresAuth: true },
        beforeEnter: requireAuth,
        props: true
    },
    {
        path: '/tasks/:id/edit',
        name: 'EditTask',
        component: TaskForm,
        meta: { requiresAuth: true },
        beforeEnter: requireAuth,
        props: true
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router 