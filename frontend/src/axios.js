import axios from 'axios'

// 🔹 Configuración base
axios.defaults.baseURL = 'http://127.0.0.1:8000/api'
axios.defaults.withCredentials = true
axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';

// 🔹 CSRF cookie (fuera de /api)
axios.get('http://127.0.0.1:8000/sanctum/csrf-cookie', { withCredentials: true })
    .then(() => {
        console.log('CSRF cookie set successfully.');
    })
    .catch(() => {
        console.error('CSRF token not found. You might not be able to login.');
    });

// 🔹 Interceptor para adjuntar el token automáticamente
axios.interceptors.request.use(
    config => {
        const token = localStorage.getItem('token')
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    },
    error => Promise.reject(error)
)

export default axios