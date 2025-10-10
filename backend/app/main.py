import logging
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes import auth, venta
from app.database import init_database, seed_initial_data

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('aplicacion.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

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

# Middleware para logging de requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.now()
    
    # Log de entrada
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    logger.info(f"Client IP: {request.client.host}")
    
    response = await call_next(request)
    
    # Calcular tiempo de procesamiento
    process_time = (datetime.now() - start_time).total_seconds()
    
    # Log de salida
    logger.info(f"Completed: {request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time:.2f}s")
    
    return response

# Incluir routers
app.include_router(auth.router)
app.include_router(venta.router)


@app.get("/")
async def root():
    """Endpoint raíz de la API"""
    logger.info("Root endpoint accessed")
    return {
        "message": "Bienvenido a la API de Automotriz JJ",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Endpoint para verificar el estado del servidor"""
    logger.info("Health check accessed")
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


# Evento de inicio
@app.on_event("startup")
async def startup_event():
    """Se ejecuta cuando la aplicación inicia"""
    logger.info("=" * 50)
    logger.info(f"🚀 Iniciando {settings.APP_NAME} v{settings.APP_VERSION}")
    
    # Inicializar base de datos
    try:
        logger.info("📊 Inicializando base de datos...")
        init_database()
        seed_initial_data()
        logger.info("✅ Base de datos lista")
    except Exception as e:
        logger.error(f"❌ Error al inicializar base de datos: {e}")
    
    logger.info(f"📝 Documentación disponible en: http://localhost:8000/docs")
    logger.info(f"🔐 Usuario de prueba: {settings.DEFAULT_USERNAME}")
    logger.info(f"🔑 Contraseña de prueba: {settings.DEFAULT_PASSWORD}")
    logger.info("=" * 50)


# Evento de cierre
@app.on_event("shutdown")
async def shutdown_event():
    """Se ejecuta cuando la aplicación se cierra"""
    logger.info("=" * 50)
    logger.info(f"👋 Cerrando {settings.APP_NAME}")
    logger.info("=" * 50)