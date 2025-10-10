import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import Modal from '../components/Modal'

const VentaAuto = () => {
  const { user } = useAuth()
  const [formData, setFormData] = useState({
    autosDisponibles: '',
    tipoCompra: '',
    montoFisco: '',
    nombreComprador: '',
    codigoVendedor: user?.codigo_vendedor || '',
    dniComprador: '',
    contactoComprador: ''
  })

  const [fechaActual, setFechaActual] = useState('')
  const [modalOpen, setModalOpen] = useState(false)
  const [modalConfig, setModalConfig] = useState({
    title: '',
    message: '',
    type: 'success'
  })

  useEffect(() => {
    // Obtener fecha actual
    const hoy = new Date()
    const opciones = { year: 'numeric', month: 'long', day: 'numeric' }
    setFechaActual(hoy.toLocaleDateString('es-ES', opciones))
  }, [])

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const validateForm = () => {
    // Validar que todos los campos estén llenos
    const requiredFields = [
      'autosDisponibles',
      'tipoCompra',
      'montoFisco',
      'nombreComprador',
      'dniComprador',
      'contactoComprador'
    ]

    for (let field of requiredFields) {
      if (!formData[field] || formData[field].trim() === '') {
        return false
      }
    }

    // Validar DNI (debe ser 8 dígitos)
    if (formData.dniComprador.length !== 8 || !/^\d+$/.test(formData.dniComprador)) {
      return 'dni'
    }

    return true
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    
    const validation = validateForm()

    if (validation === false) {
      // Mostrar modal de error
      setModalConfig({
        title: 'Gestor de Ventas',
        message: '⚠️ Es obligatorio rellenar todos los campos',
        type: 'error'
      })
      setModalOpen(true)
      return
    }

    if (validation === 'dni') {
      setModalConfig({
        title: 'Gestor de Ventas',
        message: '⚠️ El DNI debe tener exactamente 8 dígitos',
        type: 'error'
      })
      setModalOpen(true)
      return
    }

    // Si todo está bien, registrar la venta
    console.log('Datos de venta:', formData)
    console.log('Usuario:', user)
    console.log('Fecha:', fechaActual)

    // Mostrar modal de éxito
    setModalConfig({
      title: 'Gestor de Ventas',
      message: '💾 Registro de venta completado con éxito.',
      type: 'success'
    })
    setModalOpen(true)

    // Limpiar formulario después del registro exitoso
    setFormData({
      autosDisponibles: '',
      tipoCompra: '',
      montoFisco: '',
      nombreComprador: '',
      codigoVendedor: user?.codigo_vendedor || '',
      dniComprador: '',
      contactoComprador: ''
    })
  }

  const closeModal = () => {
    setModalOpen(false)
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4">
        {/* Header con información del vendedor */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <p className="text-sm text-gray-600">Fecha</p>
              <p className="font-semibold text-gray-900">{fechaActual}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Sucursal</p>
              <p className="font-semibold text-primary-blue">{user?.sucursal}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Nombre Vendedor</p>
              <p className="font-semibold text-gray-900">{user?.full_name}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Código Vendedor</p>
              <p className="font-semibold text-primary-blue">{user?.codigo_vendedor}</p>
            </div>
          </div>
        </div>

        {/* Formulario de Venta */}
        <div className="bg-white rounded-lg shadow-md p-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-6 text-center">
            Registro de Venta de Automóvil
          </h1>

          <form onSubmit={handleSubmit}>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
              {/* Columna Izquierda */}
              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Autos Disponibles <span className="text-red-500">*</span>
                  </label>
                  <select
                    name="autosDisponibles"
                    value={formData.autosDisponibles}
                    onChange={handleChange}
                    className="input-field"
                  >
                    <option value="">Seleccionar auto</option>
                    <option value="Toyota Corolla 2024">Toyota Corolla 2024</option>
                    <option value="Honda Civic 2024">Honda Civic 2024</option>
                    <option value="Nissan Sentra 2024">Nissan Sentra 2024</option>
                    <option value="Hyundai Elantra 2024">Hyundai Elantra 2024</option>
                    <option value="Mazda 3 2024">Mazda 3 2024</option>
                    <option value="Kia Forte 2024">Kia Forte 2024</option>
                    <option value="Chevrolet Cruze 2024">Chevrolet Cruze 2024</option>
                    <option value="Ford Focus 2024">Ford Focus 2024</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Tipo de Compra <span className="text-red-500">*</span>
                  </label>
                  <select
                    name="tipoCompra"
                    value={formData.tipoCompra}
                    onChange={handleChange}
                    className="input-field"
                  >
                    <option value="">Seleccionar tipo</option>
                    <option value="Cash">Cash</option>
                    <option value="Crédito">Crédito</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Monto o Fisco <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    name="montoFisco"
                    value={formData.montoFisco}
                    onChange={handleChange}
                    placeholder="Ej: S/. 50,000"
                    className="input-field"
                  />
                </div>
              </div>

              {/* Columna Derecha */}
              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Nombre del Comprador <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    name="nombreComprador"
                    value={formData.nombreComprador}
                    onChange={handleChange}
                    placeholder="Nombre completo"
                    className="input-field"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Datos del Comprador (DNI) <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    name="dniComprador"
                    value={formData.dniComprador}
                    onChange={handleChange}
                    placeholder="DNI de 8 dígitos"
                    className="input-field"
                    maxLength="8"
                    pattern="\d*"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Datos del Comprador (Contacto) <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="tel"
                    name="contactoComprador"
                    value={formData.contactoComprador}
                    onChange={handleChange}
                    placeholder="Teléfono de contacto"
                    className="input-field"
                  />
                </div>
              </div>
            </div>

            {/* Botón de VENTA */}
            <div className="flex justify-center mt-8">
              <button
                type="submit"
                className="bg-gradient-blue text-white font-bold py-4 px-16 rounded-lg
                         hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1
                         text-lg"
              >
                REGISTRAR VENTA
              </button>
            </div>
          </form>
        </div>

        {/* Información adicional */}
        <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
          <p className="text-sm text-blue-700">
            <span className="font-semibold">Nota:</span> Todos los campos marcados con 
            <span className="text-red-500 font-bold"> *</span> son obligatorios. 
            Asegúrese de verificar los datos antes de registrar la venta.
          </p>
        </div>
      </div>

      {/* Modal */}
      <Modal
        isOpen={modalOpen}
        onClose={closeModal}
        title={modalConfig.title}
        message={modalConfig.message}
        type={modalConfig.type}
      />
    </div>
  )
}

export default VentaAuto