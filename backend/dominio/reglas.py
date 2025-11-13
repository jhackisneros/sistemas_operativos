# backend/dominio/reglas.py
from backend.dominio.modelos import Conductor, EstadoConductor


def aprobar_o_rechazar_conductor(c: Conductor) -> Conductor:
    """
    Regla básica:
      - Si no tiene licencia_ok o antecedentes_ok = False → RECHAZADO
      - Si todo ok → APROBADO (luego podrá ponerse ONLINE/OFFLINE)
    """
    if not c.licencia_ok or not c.antecedentes_ok:
        c.estado = EstadoConductor.RECHAZADO
    else:
        c.estado = EstadoConductor.APROBADO
    return c
