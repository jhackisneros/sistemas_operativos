# backend/autenticacion/esquemas.py
from enum import Enum
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class Rol(str, Enum):
    CONDUCTOR = "CONDUCTOR"
    PASAJERO  = "PASAJERO"
    ADMIN     = "ADMIN"


class RegistroEntrada(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=80)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)
    rol: Rol


class InicioEntrada(BaseModel):
    email: EmailStr
    password: str


class Usuario(BaseModel):
    id: str
    nombre: str
    email: EmailStr
    rol: Rol
    activo: bool = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenDatos(BaseModel):
    sub: str  # user_id
    email: EmailStr
    rol: Rol
