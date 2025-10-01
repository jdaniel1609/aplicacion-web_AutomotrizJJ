import axios from 'axios'
import { getStoredToken } from '../utils/auth'

// Configuración base de la API
const API_BASE_URL = 'http://localhost:8000'  // Cambia por la URL de tu FastAPI

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Interceptor para agregar el token a todas las peticiones
apiClient.interceptors.request.use(
  (config) => {
    const token = getStoredToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Interceptor para manejar respuestas y errores
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expirado o inválido
      localStorage.removeItem('auth_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Función para login
export const loginUser = async (username, password) => {
  try {
    // FastAPI generalmente espera form data para OAuth2
    const formData = new FormData()
    formData.append('username', username)
    formData.append('password', password)

    const response = await apiClient.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })
    
    return response.data
  } catch (error) {
    throw error
  }
}

// Función para obtener perfil del usuario
export const getUserProfile = async () => {
  try {
    const response = await apiClient.get('/auth/me')
    return response.data
  } catch (error) {
    throw error
  }
}

// Función para verificar el estado del servidor
export const checkServerHealth = async () => {
  try {
    const response = await apiClient.get('/health')
    return response.data
  } catch (error) {
    throw error
  }
}

export default apiClient