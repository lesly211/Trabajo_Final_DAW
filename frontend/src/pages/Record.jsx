import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import PageHeader from "../components/PageHeader";
import Kpi from "../components/Kpi";
import Badge from "../components/Badge";
import { recordApi } from "../api/endpoints";

export default function Record() {
  const { usuario } = useAuth();
  const [data, setData] = useState(null);
  const [consolidado, setConsolidado] = useState([]);

  useEffect(() => {
    if (usuario.rol === "estudiante") {
      recordApi.estudiante(usuario.id).then((r) => setData(r.data));
    } else {
      recordApi.consolidado().then((r) => setConsolidado(r.data));
    }
  }, []);

  if (usuario.rol !== "estudiante") {
    return (
      <>
        <PageHeader tag="Módulo 4" title="Reportes Consolidados"
          subtitle="Desempeño académico por estudiante y programa." />
        <div className="content">
          <div className="card">
            <table className="tabla">
              <thead><tr><th>Estudiante</th><th>Especialidad</th><th>Cursos</th><th>Promedio</th></tr></thead>
              <tbody>
                {consolidado.map((c, i) => (
                  <tr key={i}>
                    <td>{c.estudiante}</td><td>{c.especialidad}</td>
                    <td>{c.cursos}</td><td><b>{c.promedio}</b></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </>
    );
  }

  return (
    <>
      <PageHeader tag="Módulo 4" title="Record Académico"
        subtitle="Su historial académico completo." />
      <div className="content">
        {data && (
          <>
            <div className="grid grid-3 mb-2">
              <Kpi label="Promedio ponderado" value={data.resumen.promedio_ponderado} />
              <Kpi label="Créditos aprobados"
                value={`${data.resumen.creditos_aprobados} / ${data.resumen.creditos_totales}`} />
              <Kpi label="Cursos llevados" value={data.resumen.cursos_llevados} />
            </div>
            <div className="card">
              <div className="card-title">Historial de cursos</div>
              <table className="tabla">
                <thead><tr><th>Código</th><th>Curso</th><th>Periodo</th>
                  <th>Cr.</th><th>Promedio</th><th>Estado</th></tr></thead>
                <tbody>
                  {data.cursos.map((c) => (
                    <tr key={c.id}>
                      <td><b>{c.codigo}</b></td><td>{c.curso}</td><td>{c.periodo}</td>
                      <td>{c.creditos}</td><td><b>{c.promedio}</b></td>
                      <td><Badge estado={c.estado} /></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </>
        )}
      </div>
    </>
  );
}
