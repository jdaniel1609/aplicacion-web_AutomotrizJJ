import { createContext, useContext, useState, useEffect } from 'react'
import { loginUser } from '../services/api'
import { getStoredToken, setStoredToken, removeStoredToken } from '../utils/auth'

const AuthContext = createContext()

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = getStoredToken()
    if (token) {
      setIsAuthenticated(true)
      // Aquí podrías hacer una llamada para obtener los datos del usuario
      setUser({ token })
    }
    setLoading(false)
  }, [])

  const login = async (username, password) => {
    try {
      setLoading(true)
      const response = await loginUser(username, password)
      
      if (response.access_token) {
        setStoredToken(response.access_token)
        setUser({ 
          token: response.access_token,
          username: username 
        })
        setIsAuthenticated(true)
        return { success: true }
      }
      
      return { success: false, error: 'Credenciales inválidas' }
    } catch (error) {
      console.error('Error en login:', error)
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Error de conexión con el servidor' 
      }
    } finally {
      setLoading(false)
    }
  }

  const logout = () => {
    removeStoredToken()
    setUser(null)
    setIsAuthenticated(false)
  }

  const value = {
    user,
    isAuthenticated,
    loading,
    login,
    logout
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}