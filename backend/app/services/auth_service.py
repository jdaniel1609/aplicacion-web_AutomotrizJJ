from typing import Optional
from app.utils.security import verify_password, get_password_hash
from app.config import settings


# Base de datos en memoria para desarrollo (usuarios hardcodeados)
# En producción, esto debería ser reemplazado por una base de datos real
FAKE_USERS_DB = {
    "admin": {
        "username": "admin",
        "full_name": "Administrador",
        "email": "admin@automotrizjj.com",
        "hashed_password": "",  # Se inicializará en el primer uso
        "is_active": True,
    }
}


def init_default_user():
    """Inicializa el usuario por defecto con la contraseña hasheada"""
    if not FAKE_USERS_DB["admin"]["hashed_password"]:
        FAKE_USERS_DB["admin"]["hashed_password"] = get_password_hash(
            settings.DEFAULT_PASSWORD
        )


def authenticate_user(username: str, password: str) -> Optional[dict]:
    """
    Autentica un usuario verificando sus credenciales
    
    Args:
        username: Nombre de usuario
        password: Contraseña en texto plano
        
    Returns:
        dict: Datos del usuario si las credenciales son válidas
        None: Si las credenciales son inválidas
    """
    # Inicializar usuario por defecto si es necesario
    init_default_user()
    
    # Buscar usuario en la base de datos fake
    user = FAKE_USERS_DB.get(username)
    
    if not user:
        return None
    
    # Verificar contraseña
    if not verify_password(password, user["hashed_password"]):
        return None
    
    # Verificar que el usuario esté activo
    if not user.get("is_active", False):
        return None
    
    return user


def get_user(username: str) -> Optional[dict]:
    """
    Obtiene un usuario por su nombre de usuario
    
    Args:
        username: Nombre de usuario
        
    Returns:
        dict: Datos del usuario si existe
        None: Si no existe
    """
    init_default_user()
    return FAKE_USERS_DB.get(username)


def create_user(username: str, password: str, email: str = None, full_name: str = None) -> dict:
    """
    Crea un nuevo usuario
    
    Args:
        username: Nombre de usuario
        password: Contraseña en texto plano
        email: Email del usuario (opcional)
        full_name: Nombre completo (opcional)
        
    Returns:
        dict: Datos del usuario creado
    """
    if username in FAKE_USERS_DB:
        raise ValueError("El usuario ya existe")
    
    user_data = {
        "username": username,
        "email": email,
        "full_name": full_name,
        "hashed_password": get_password_hash(password),
        "is_active": True,
    }
    
    FAKE_USERS_DB[username] = user_data
    return user_data