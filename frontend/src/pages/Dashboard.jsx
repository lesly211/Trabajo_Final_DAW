import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import PageHeader from "../components/PageHeader";
import Kpi from "../components/Kpi";
import { matriculaApi, notaApi, recordApi } from "../api/endpoints";

export default function Dashboard() {
  const { usuario } = useAuth();
  const [data, setData] = useState({});

  useEffect(() => {
    const r = usuario.rol;
    if (r === "direccion" || r === "admin") {
      Promise.all([
        matriculaApi.estadisticas().catch(() => ({ data: {} })),
        notaApi.indicadores().catch(() => ({ data: {} })),
      ]).then(([m, n]) => setData({ matricula: m.data, notas: n.data }));
    } else if (r === "estudiante") {
      recordApi.estudiante(usuario.id).then((res) => setData({ record: res.data.resumen }));
    }
  }, [usuario]);

  return (
    <>
      <PageHeader tag={`Bienvenido, ${usuario.nombres}`} title="Panel principal"
        subtitle="Resumen de su actividad académica." />
      <div className="content">
        {(usuario.rol === "direccion" || usuario.rol === "admin") && (
          <>
            <div className="grid grid-3 mb-2">
              <Kpi label="Matrículas totales" value={data.matricula?.total ?? "—"} />
              <Kpi label="Ingresos registrados" value={`S/ ${data.matricula?.ingresos ?? 0}`} />
              <Kpi label="Tasa de aprobación" value={`${data.notas?.tasa_aprobacion ?? 0}%`}
                sub={`Promedio general: ${data.notas?.promedio_general ?? 0}`} />
            </div>
            <div className="grid grid-3">
              <Kpi label="Actas evaluadas" value={data.notas?.total ?? 0} />
              <Kpi label="Aprobados" value={data.notas?.aprobados ?? 0} />
              <Kpi label="Desaprobados" value={data.notas?.desaprobados ?? 0} />
            </div>
          </>
        )}

        {usuario.rol === "estudiante" && (
          <div className="grid grid-3">
            <Kpi label="Promedio ponderado" value={data.record?.promedio_ponderado ?? "—"} />
            <Kpi label="Créditos aprobados"
              value={`${data.record?.creditos_aprobados ?? 0} / ${data.record?.creditos_totales ?? 0}`} />
            <Kpi label="Cursos llevados" value={data.record?.cursos_llevados ?? 0} />
          </div>
        )}

        {usuario.rol === "docente" && (
          <div className="card">
            <div className="card-title">Acceso rápido</div>
            <p className="muted">
              Use el menú lateral para ver sus cursos asignados, cargar sílabos y
              registrar las notas parciales y finales de sus estudiantes.
            </p>
          </div>
        )}
      </div>
    </>
  );
}
