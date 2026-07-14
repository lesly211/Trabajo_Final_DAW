import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import PageHeader from "../components/PageHeader";
import Badge from "../components/Badge";
import Toast from "../components/Toast";
import { matriculaApi, cursoApi } from "../api/endpoints";

export default function Matricula() {
  const { usuario } = useAuth();
  const esEstudiante = usuario.rol === "estudiante";
  const [lista, setLista] = useState([]);
  const [cursos, setCursos] = useState([]);
  const [seleccion, setSeleccion] = useState([]);
  const [toast, setToast] = useState("");

  const cargar = () => matriculaApi.listar().then((r) => setLista(r.data));

  useEffect(() => {
    cargar();
    if (esEstudiante) cursoApi.listar().then((r) => setCursos(r.data));
  }, []);

  const toggle = (id) =>
    setSeleccion((s) => (s.includes(id) ? s.filter((x) => x !== id) : [...s, id]));

  const solicitar = async () => {
    if (!seleccion.length) return;
    try {
      await matriculaApi.solicitar({ periodo: "2026-I", cursos: seleccion });
      setSeleccion([]);
      setToast("Matrícula solicitada correctamente.");
      cargar();
    } catch (e) {
      setToast(e.response?.data?.error || "No se pudo registrar la solicitud de matrícula.");
    }
  };

  const validar = async (id, aprobar) => {
    try {
      await matriculaApi.validar(id, { aprobar, pago: aprobar, monto: 350 });
      setToast(aprobar ? "Matrícula validada y pago registrado." : "Matrícula rechazada.");
      cargar();
    } catch (e) {
      setToast(e.response?.data?.error || "No se pudo procesar la solicitud.");
    }
  };

  const descargarFicha = async (m) => {
    try {
      const r = await matriculaApi.descargarFicha(m.id);
      const url = window.URL.createObjectURL(new Blob([r.data], { type: "application/pdf" }));
      const a = document.createElement("a");
      a.href = url;
      a.download = `ficha_matricula_${m.periodo}_${m.id}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch {
      setToast("No se pudo descargar la ficha de matrícula.");
    }
  };

  return (
    <>
      <PageHeader tag="Módulo 1" title="Matrícula"
        subtitle={esEstudiante ? "Solicite su matrícula y descargue su ficha."
          : "Valide requisitos, registre pagos y genere la ficha oficial."} />
      <div className="content">
        {esEstudiante && (
          <div className="card mb-2">
            <div className="card-title">Solicitar matrícula — Periodo 2026-I</div>
            <div className="grid grid-2">
              {cursos.map((c) => (
                <label key={c.id} className="row" style={{ cursor: "pointer" }}>
                  <input type="checkbox" checked={seleccion.includes(c.id)}
                    onChange={() => toggle(c.id)} />
                  <span><b>{c.codigo}</b> · {c.nombre} ({c.creditos} cr.)</span>
                </label>
              ))}
            </div>
            <button className="btn btn-primary mt-2" onClick={solicitar}
              disabled={!seleccion.length}>
              Solicitar matrícula ({seleccion.length})
            </button>
          </div>
        )}

        <div className="card">
          <div className="card-title">
            {esEstudiante ? "Mis matrículas" : "Solicitudes de matrícula"}
          </div>
          {lista.length === 0 ? (
            <div className="empty">No hay matrículas registradas.</div>
          ) : (
            <table className="tabla">
              <thead>
                <tr>
                  {!esEstudiante && <th>Estudiante</th>}
                  <th>Periodo</th><th>Cursos</th><th>Monto</th>
                  <th>Estado</th><th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {lista.map((m) => (
                  <tr key={m.id}>
                    {!esEstudiante && <td>{m.estudiante}</td>}
                    <td>{m.periodo}</td>
                    <td>{m.cursos.length}</td>
                    <td>S/ {m.monto}</td>
                    <td><Badge estado={m.estado} /></td>
                    <td>
                      <div className="row">
                        {esEstudiante && m.estado === "validada" && (
                          <button className="btn btn-outline btn-sm"
                            onClick={() => descargarFicha(m)}>Descargar ficha</button>
                        )}
                        {usuario.rol === "admin" && m.estado === "pendiente" && (
                          <>
                            <button className="btn btn-primary btn-sm"
                              onClick={() => validar(m.id, true)}>Validar</button>
                            <button className="btn btn-outline btn-sm"
                              onClick={() => validar(m.id, false)}>Rechazar</button>
                          </>
                        )}
                        {usuario.rol === "admin" && m.estado === "validada" && (
                          <button className="btn btn-outline btn-sm"
                            onClick={() => descargarFicha(m)}>Ficha oficial</button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
      <Toast mensaje={toast} onClose={() => setToast("")} />
    </>
  );
}
