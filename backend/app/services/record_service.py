"""Cálculo del record académico y métricas."""
from ..models.nota import Nota


def record_estudiante(estudiante_id):
    notas = Nota.query.filter_by(estudiante_id=estudiante_id, validada=True).all()
    cursos = [n.to_dict() for n in notas]

    creditos_totales = sum(c["creditos"] or 0 for c in cursos)
    creditos_aprobados = sum(
        (c["creditos"] or 0) for c in cursos if (c["promedio"] or 0) >= 10.5
    )
    promedios = [c["promedio"] for c in cursos if c["promedio"] is not None]
    promedio_ponderado = (
        round(sum((c["promedio"] or 0) * (c["creditos"] or 0) for c in cursos) /
              creditos_totales, 2)
        if creditos_totales else 0
    )

    return {
        "cursos": cursos,
        "resumen": {
            "creditos_totales": creditos_totales,
            "creditos_aprobados": creditos_aprobados,
            "cursos_llevados": len(cursos),
            "promedio_ponderado": promedio_ponderado,
        },
    }
