import LoginForm from '../components/LoginForm'

const Login = () => {
  return (
    <div className="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="w-full max-w-6xl">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
          {/* Panel izquierdo - Información de la empresa */}
          <div className="hidden lg:block">
            <div className="bg-gradient-blue rounded-2xl p-12 text-white h-full min-h-[600px] flex flex-col justify-center relative overflow-hidden">
              <div className="space-y-6 relative z-10">
                <div>
                  <h1 className="text-4xl font-bold mb-2">
                    Employer Medical Portal
                  </h1>
                  <div className="w-16 h-1 bg-white/30 rounded-full"></div>
                </div>
                
                <div className="space-y-4 text-white/90">
                  <div className="flex items-start space-x-3">
                    <div className="w-2 h-2 bg-white rounded-full mt-2 flex-shrink-0"></div>
                    <span>Quick treatment</span>
                  </div>
                  <div className="flex items-start space-x-3">
                    <div className="w-2 h-2 bg-white rounded-full mt-2 flex-shrink-0"></div>
                    <span>Healthcare analytics</span>
                  </div>
                  <div className="flex items-start space-x-3">
                    <div className="w-2 h-2 bg-white rounded-full mt-2 flex-shrink-0"></div>
                    <span>Easy scheduling</span>
                  </div>
                  <div className="flex items-start space-x-3">
                    <div className="w-2 h-2 bg-white rounded-full mt-2 flex-shrink-0"></div>
                    <span>Health assessment</span>
                  </div>
                </div>

                <div className="pt-8">
                  <p className="text-white/80 text-lg leading-relaxed">
                    Bienvenido al portal de gestión empresarial de Automotriz JJ. 
                    Accede a nuestras herramientas especializadas para optimizar 
                    la operación y el servicio al cliente.
                  </p>
                </div>
              </div>

              {/* Decorative dots pattern */}
              <div className="absolute bottom-8 left-8">
                <div className="grid grid-cols-4 gap-2">
                  {Array.from({ length: 16 }, (_, i) => (
                    <div key={i} className="w-1 h-1 bg-white/20 rounded-full"></div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Panel derecho - Formulario de login */}
          <div className="flex flex-col justify-center">
            <div className="text-center mb-8 lg:hidden">
              <h1 className="text-3xl font-bold gradient-text mb-2">
                Bienvenido, Automotriz JJ
              </h1>
              <p className="text-gray-600">Ingresa tus credenciales para continuar</p>
            </div>

            <div className="hidden lg:block text-center mb-8">
              <h2 className="text-3xl font-bold text-gray-900 mb-2">
                Bienvenido, Automotriz JJ
              </h2>
              <p className="text-gray-600">Ingresa tus credenciales para acceder al sistema</p>
            </div>

            <LoginForm />
          </div>
        </div>
      </div>
    </div>
  )
}

export default Login