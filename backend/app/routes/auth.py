from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.token import Token
from app.schemas.user import UserResponse
from app.services.auth_service import authenticate_user
from app.utils.security import create_access_token, get_current_user
from app.config import settings

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint de login para autenticar usuarios
    
    Recibe credenciales mediante OAuth2PasswordRequestForm:
    - username: Nombre de usuario
    - password: Contraseña
    
    Retorna un token JWT si las credenciales son válidas
    """
    # Autenticar usuario
    user = authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Crear token de acceso
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=dict)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """
    Obtiene la información del usuario autenticado actualmente
    
    Requiere autenticación mediante Bearer token
    """
    return {
        "username": current_user["username"],
        "message": f"Usuario autenticado: {current_user['username']}"
    }


@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    """
    Endpoint de logout (el token se invalida en el cliente)
    
    En una implementación real, aquí podrías:
    - Agregar el token a una lista negra
    - Invalidar el token en la base de datos
    - Registrar la acción de logout
    """
    return {
        "message": f"Usuario {current_user['username']} ha cerrado sesión exitosamente"
    }