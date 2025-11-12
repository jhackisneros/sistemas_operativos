# backend/autenticacion/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Callable, Dict, Any

from .servicio import decodificar_token, buscar_usuario_por_id
from .esquemas import Rol, Usuario

# Nota: tokenUrl apunta a la ruta de login que expongas (p.ej. /auth/login)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def obtener_usuario_actual(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    try:
        td = decodificar_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    row = buscar_usuario_por_id(td.sub)
    if not row or not row.get("activo", True):
        raise HTTPException(status_code=401, detail="Usuario no encontrado o inactivo")
    return row  # dict crudo; si prefieres, convierte a pydantic

def requiere_rol(rol: Rol) -> Callable:
    async def _check(user: Dict[str, Any] = Depends(obtener_usuario_actual)):
        if user.get("rol") != rol.value:
            raise HTTPException(status_code=403, detail=f"Se requiere rol {rol.value}")
        return user
    return _check

def permite_roles(*roles: Rol) -> Callable:
    valores = {r.value for r in roles}
    async def _check(user: Dict[str, Any] = Depends(obtener_usuario_actual)):
        if user.get("rol") not in valores:
            raise HTTPException(status_code=403, detail=f"Acceso restringido a roles: {', '.join(valores)}")
        return user
    return _check
