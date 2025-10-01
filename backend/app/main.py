from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes import auth

# Crear instancia de FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API para el sistema de gestión de Automotriz JJ",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router)


@app.get("/")
async def root():
    """Endpoint raíz de la API"""
    return {
        "message": "Bienvenido a la API de Automotriz JJ",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Endpoint para verificar el estado del servidor"""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


# Evento de inicio
@app.on_event("startup")
async def startup_event():
    """Se ejecuta cuando la aplicación inicia"""
    print(f"🚀 Iniciando {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"📝 Documentación disponible en: http://localhost:8000/docs")
    print(f"🔐 Usuario de prueba: {settings.DEFAULT_USERNAME}")
    print(f"🔑 Contraseña de prueba: {settings.DEFAULT_PASSWORD}")


# Evento de cierre
@app.on_event("shutdown")
async def shutdown_event():
    """Se ejecuta cuando la aplicación se cierra"""
    print(f"👋 Cerrando {settings.APP_NAME}")