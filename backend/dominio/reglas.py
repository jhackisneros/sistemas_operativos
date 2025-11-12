# backend/dominio/reglas.py
from .modelos import Conductor, EstadoConductor


def aprobar_o_rechazar_conductor(c: Conductor) -> Conductor:
    """
    Regla mínima:
      - Si antecedentes_ok == False -> RECHAZADO
      - Si licencia_ok == True y sin antecedentes -> APROBADO
      - En otro caso -> PENDIENTE
    """
    if not c.antecedentes_ok:
        c.estado = EstadoConductor.RECHAZADO
    elif c.licencia_ok:
        c.estado = EstadoConductor.APROBADO
    else:
        c.estado = EstadoConductor.PENDIENTE
    return c
