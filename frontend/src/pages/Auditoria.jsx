import { useEffect, useState } from "react";
import PageHeader from "../components/PageHeader";
import { seguridadApi } from "../api/endpoints";
import { rolLabel } from "../utils/format";

export default function Auditoria() {
  const [logs, setLogs] = useState([]);
  useEffect(() => { seguridadApi.auditoria().then((r) => setLogs(r.data)); }, []);

  return (
    <>
      <PageHeader tag="Módulo 6" title="Auditoría del Sistema"
        subtitle="Registro de acciones para control y reportes estratégicos." />
      <div className="content">
        <div className="card">
          <div className="card-title">Eventos recientes ({logs.length})</div>
          <table className="tabla">
            <thead><tr><th>Fecha</th><th>Usuario</th><th>Rol</th>
              <th>Módulo</th><th>Acción</th><th>Detalle</th></tr></thead>
            <tbody>
              {logs.map((l) => (
                <tr key={l.id}>
                  <td>{l.fecha}</td>
                  <td>{l.usuario}</td>
                  <td>{l.rol ? rolLabel[l.rol] : "—"}</td>
                  <td>{l.modulo || "—"}</td>
                  <td>{l.accion}</td>
                  <td className="muted">{l.detalle || "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
}
