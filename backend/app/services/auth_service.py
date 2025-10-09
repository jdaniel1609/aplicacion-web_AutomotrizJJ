from typing import Optional
import hashlib


# Base de datos en memoria con vendedores
FAKE_USERS_DB = {
    "admin": {
        "username": "admin",
        "full_name": "Administrador",
        "email": "admin@automotrizjj.com",
        "hashed_password": hashlib.sha256("admin123".encode()).hexdigest(),
        "is_active": True,
        "role": "admin",
        "codigo_vendedor": "ADM001",
        "sucursal": "LIMA"
    },
    "omargonzales": {
        "username": "omargonzales",
        "full_name": "Omar Gonzales",
        "email": "ogonzales@automotrizjj.com",
        "hashed_password": hashlib.sha256("omar2024".encode()).hexdigest(),
        "is_active": True,
        "role": "vendedor",
        "codigo_vendedor": "VEN001",
        "sucursal": "PIURA"
    },
    "ciroramirez": {
        "username": "ciroramirez",
        "full_name": "Ciro Ramírez",
        "email": "cramirez@automotrizjj.com",
        "hashed_password": hashlib.sha256("ciro2024".encode()).hexdigest(),
        "is_active": True,
        "role": "vendedor",
        "codigo_vendedor": "VEN002",
        "sucursal": "LIMA"
    },
    "juanperez": {
        "username": "juanperez",
        "full_name": "Juan Pérez",
        "email": "jperez@automotrizjj.com",
        "hashed_password": hashlib.sha256("juan2024".encode()).hexdigest(),
        "is_active": True,
        "role": "vendedor",
        "codigo_vendedor": "VEN003",
        "sucursal": "AREQUIPA"
    },
    "luciatores": {
        "username": "luciatorres",
        "full_name": "Lucía Torres",
        "email": "ltorres@automotrizjj.com",
        "hashed_password": hashlib.sha256("lucia2024".encode()).hexdigest(),
        "is_active": True,
        "role": "vendedor",
        "codigo_vendedor": "VEN004",
        "sucursal": "LIMA"
    },
    "valeriasanchez": {
        "username": "valeriasanchez",
        "full_name": "Valeria Sánchez",
        "email": "vsanchez@automotrizjj.com",
        "hashed_password": hashlib.sha256("valeria2024".encode()).hexdigest(),
        "is_active": True,
        "role": "vendedor",
        "codigo_vendedor": "VEN005",
        "sucursal": "PIURA"
    },
    "angelicaflores": {
        "username": "angelicaflores",
        "full_name": "Angélica Flores",
        "email": "aflores@automotrizjj.com",
        "hashed_password": hashlib.sha256("angelica2024".encode()).hexdigest(),
        "is_active": True,
        "role": "vendedor",
        "codigo_vendedor": "VEN006",
        "sucursal": "AREQUIPA"
    }
}


def simple_verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verificación simple de contraseña para desarrollo"""
    return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password


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
    # Buscar usuario en la base de datos fake
    user = FAKE_USERS_DB.get(username)
    
    if not user:
        print(f"❌ Usuario no encontrado: {username}")
        return None
    
    # Verificar contraseña
    if not simple_verify_password(password, user["hashed_password"]):
        print(f"❌ Contraseña incorrecta para usuario: {username}")
        return None
    
    # Verificar que el usuario esté activo
    if not user.get("is_active", False):
        print(f"❌ Usuario inactivo: {username}")
        return None
    
    print(f"✅ Autenticación exitosa para usuario: {username}")
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
    return FAKE_USERS_DB.get(username)