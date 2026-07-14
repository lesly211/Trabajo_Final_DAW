import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import PageHeader from "../components/PageHeader";
import Toast from "../components/Toast";
import { cursoApi } from "../api/endpoints";

export default function Cursos() {
  const { usuario } = useAuth();
  const rol = usuario.rol;
  const [cursos, setCursos] = useState([]);
  const [docentes, setDocentes] = useState([]);
  const [carga, setCarga] = useState([]);
  const [toast, setToast] = useState("");

  const cargar = () => {
    const params = rol === "docente" ? { mios: 1 } : {};
    cursoApi.listar(params).then((r) => setCursos(r.data));
  };

  useEffect(() => {
    cargar();
    if (rol === "admin") cursoApi.docentes().then((r) => setDocentes(r.data));
    if (rol === "direccion") cursoApi.cargaDocente().then((r) => setCarga(r.data));
  }, []);

  const cargarSilabo = async (id) => {
    await cursoApi.cargarSilabo(id, { silabo_url: "silabo_2026I.pdf" });
    setToast("Sílabo cargado correctamente.");
    cargar();
  };

  const asignar = async (id, docente_id, horario) => {
    await cursoApi.asignar(id, { docente_id: Number(docente_id), horario });
    setToast("Docente/horario actualizado.");
    cargar();
  };

  // Vista Dirección: carga docente
  if (rol === "direccion") {
    return (
      <>
        <PageHeader tag="Módulo 2" title="Carga Docente"
          subtitle="Evalúe la carga docente y el cumplimiento del plan de estudios." />
        <div className="content">
          <div className="card">
            <div className="card-title">Distribución de carga por docente</div>
            <table className="tabla">
              <thead><tr><th>Docente</th><th>Cursos</th><th>Créditos</th></tr></thead>
              <tbody>
                {carga.map((c, i) => (
                  <tr key={i}><td>{c.docente}</td><td>{c.cursos}</td><td>{c.creditos}</td></tr>
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
      <PageHeader tag="Módulo 2" title={rol === "docente" ? "Mis Cursos" : "Cursos y Docentes"}
        subtitle={rol === "docente" ? "Cursos asignados — cargue sílabos."
          : "Asigne docentes y gestione horarios."} />
      <div className="content">
        <div className="card">
          <table className="tabla">
            <thead>
              <tr><th>Código</th><th>Curso</th><th>Ciclo</th><th>Cr.</th>
                <th>Docente</th><th>Horario</th><th>Sílabo</th><th></th></tr>
            </thead>
            <tbody>
              {cursos.map((c) => (
                <tr key={c.id}>
                  <td><b>{c.codigo}</b></td>
                  <td>{c.nombre}</td>
                  <td>{c.ciclo}</td>
                  <td>{c.creditos}</td>
                  <td>
                    {rol === "admin" ? (
                      <select defaultValue={c.docente_id || ""} id={`doc-${c.id}`}
                        className="field" style={{ margin: 0 }}>
                        <option value="">— sin asignar —</option>
                        {docentes.map((d) => (
                          <option key={d.id} value={d.id}>{d.nombre_completo}</option>
                        ))}
                      </select>
                    ) : (c.docente || "—")}
                  </td>
                  <td>
                    {rol === "admin" ? (
                      <input defaultValue={c.horario || ""} id={`hor-${c.id}`}
                        className="field" style={{ margin: 0, width: 110 }} />
                    ) : (c.horario || "—")}
                  </td>
                  <td>{c.silabo_url ? <span className="badge badge-ok">Cargado</span>
                    : <span className="badge badge-neutral">Pendiente</span>}</td>
                  <td>
                    {rol === "docente" && (
                      <button className="btn btn-outline btn-sm"
                        onClick={() => cargarSilabo(c.id)}>Cargar sílabo</button>
                    )}
                    {rol === "admin" && (
                      <button className="btn btn-primary btn-sm" onClick={() =>
                        asignar(c.id,
                          document.getElementById(`doc-${c.id}`).value,
                          document.getElementById(`hor-${c.id}`).value)}>
                        Guardar</button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
      <Toast mensaje={toast} onClose={() => setToast("")} />
    </>
  );
}
