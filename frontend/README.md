# SynergySphere Frontend

This is the frontend application for SynergySphere, an advanced team collaboration platform built with Vue 3.

## Features

- User authentication (sign up and login)
- Project management (create, view, edit, delete projects)
- Task management (create, view, edit, delete tasks)
- My Tasks view to see tasks assigned to you
- Responsive desktop layout

## Project Setup

### Install dependencies
```
npm install
```

### Compile and hot-reload for development
```
npm run serve
```

### Compile and minify for production
```
npm run build
```

### Run linter
```
npm run lint
```

## Backend API

This frontend application connects to a Flask backend API. Make sure the backend is running at http://localhost:5000 or update the API_URL in `src/store/index.js` and `src/services/api.js` to match your backend URL.

## Pages
- Login
- Sign Up
- Projects (dashboard)
- Project Tasks
- My Tasks
- Project Create/Edit
- Task Create/Edit 