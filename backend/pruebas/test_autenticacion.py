# backend/pruebas/test_autenticacion.py
import pytest
from autenticacion.esquemas import Rol
from autenticacion.servicio import (
    crear_usuario, autenticar_usuario, emitir_token_para_usuario, decodificar_token
)

def test_registro_y_login_basico():
    u = crear_usuario("Pepe", "pepe@example.com", "secreto123", Rol.PASAJERO)
    assert u.email == "pepe@example.com"
    assert u.rol == Rol.PASAJERO

    u2 = autenticar_usuario("pepe@example.com", "secreto123")
    assert u2 is not None
    assert u2.email == "pepe@example.com"

def test_jwt_emision_y_decode():
    u = crear_usuario("Lola", "lola@example.com", "clave456", Rol.CONDUCTOR)
    token = emitir_token_para_usuario(u)
    td = decodificar_token(token)
    assert td.email == "lola@example.com"
    assert td.rol == "CONDUCTOR"
