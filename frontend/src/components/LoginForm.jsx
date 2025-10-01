import { useState } from 'react'
import { useAuth } from '../context/AuthContext'

const LoginForm = () => {
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  })
  const [error, setError] = useState('')
  const { login, loading } = useAuth()

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
    setError('') // Limpiar error cuando el usuario escribe
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!formData.username.trim() || !formData.password.trim()) {
      setError('Por favor complete todos los campos')
      return
    }

    const result = await login(formData.username, formData.password)
    
    if (!result.success) {
      setError(result.error)
    }
  }

  return (
    <div className="card p-8 w-full max-w-md">
      <div className="text-center mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Login</h2>
        <div className="w-12 h-1 bg-gradient-blue mx-auto rounded-full"></div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label htmlFor="username" className="block text-sm font-medium text-gray-700 mb-2">
            Usuario
          </label>
          <input
            type="text"
            id="username"
            name="username"
            value={formData.username}
            onChange={handleChange}
            className="input-field"
            placeholder="Ingresa tu usuario"
            disabled={loading}
          />
        </div>

        <div>
          <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
            Contraseña
          </label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            className="input-field"
            placeholder="Ingresa tu contraseña"
            disabled={loading}
          />
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={loading}
          className={`w-full btn-primary ${
            loading ? 'opacity-50 cursor-not-allowed' : ''
          }`}
        >
          {loading ? 'Iniciando sesión...' : 'Iniciar Sesión'}
        </button>
      </form>

      {/* Información de prueba (remover en producción) */}
      <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg text-xs text-blue-700">
        <p className="font-semibold mb-1">Datos de prueba:</p>
        <p>Usuario: admin</p>
        <p>Contraseña: admin123</p>
      </div>
    </div>
  )
}

export default LoginForm