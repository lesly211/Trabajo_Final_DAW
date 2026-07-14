import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import PageHeader from "../components/PageHeader";
import Badge from "../components/Badge";
import Toast from "../components/Toast";
import { notaApi, cursoApi } from "../api/endpoints";

export default function Notas() {
  const { usuario } = useAuth();
  const rol = usuario.rol;
  const [notas, setNotas] = useState([]);
  const [cursos, setCursos] = useState([]);
  const [estudiantes, setEstudiantes] = useState([]);
  const [consolidado, setConsolidado] = useState([]);
  const [cursoSel, setCursoSel] = useState("");
  const [form, setForm] = useState({ estudiante_id: "", parcial1: "", parcial2: "", final: "" });
  const [toast, setToast] = useState("");

  const cargarNotas = (params = {}) => notaApi.listar(params).then((r) => setNotas(r.data));
  const cargarConsolidado = () => notaApi.consolidado().then((r) => setConsolidado(r.data));

  useEffect(() => {
    cargarNotas();
    if (rol === "docente") {
      cursoApi.listar({ mios: 1 }).then((r) => setCursos(r.data));
    }
    if (rol === "admin") {
      cargarConsolidado();
    }
  }, []);

  // Docente selecciona un curso -> carga sus estudiantes matriculados y filtra la tabla
  useEffect(() => {
    if (rol !== "docente") return;
    if (!cursoSel) { setEstudiantes([]); return; }
    notaApi.estudiantesCurso(cursoSel).then((r) => setEstudiantes(r.data));
    cargarNotas({ curso_id: cursoSel });
  }, [cursoSel]);

  const registrar = async () => {
    if (!cursoSel || !form.estudiante_id) return setToast("Seleccione curso y estudiante.");
    try {
      await notaApi.registrar({
        curso_id: Number(cursoSel),
        estudiante_id: Number(form.estudiante_id),
        periodo: "2026-I",
        parcial1: form.parcial1 || null,
        parcial2: form.parcial2 || null,
        final: form.final || null,
      });
      setToast("Notas registradas.");
      setForm({ estudiante_id: "", parcial1: "", parcial2: "", final: "" });
      cargarNotas({ curso_id: cursoSel });
    } catch (e) {
      setToast(e.response?.data?.error || "No se pudo registrar la nota.");
    }
  };

  const validar = async (id) => {
    await notaApi.validar(id);
    setToast("Acta validada.");
    cargarNotas();
    if (rol === "admin") cargarConsolidado();
  };

  const consolidar = async (curso_id, periodo) => {
    try {
      const r = await notaApi.consolidar(curso_id, periodo);
      setToast(`Acta consolidada: ${r.data.consolidadas} notas validadas.`);
      cargarNotas();
      cargarConsolidado();
    } catch (e) {
      setToast(e.response?.data?.error || "No se pudo consolidar el acta.");
    }
  };

  return (
    <>
      <PageHeader tag="Módulo 3" title={
        rol === "estudiante" ? "Mis Notas" : rol === "admin" ? "Validación de Actas" : "Registro de Notas"
      } subtitle={
        rol === "estudiante" ? "Consulte su hoja de notas por ciclo."
          : rol === "admin" ? "Valide y consolide las actas de notas."
          : "Registre notas parciales y finales."
      } />
      <div className="content">
        {rol === "docente" && (
          <div className="card mb-2">
            <div className="card-title">Registrar nota</div>
            <div className="grid grid-3">
              <div className="field">
                <label>Curso</label>
                <select value={cursoSel} onChange={(e) => {
                  setCursoSel(e.target.value);
                  setForm({ ...form, estudiante_id: "" });
                }}>
                  <option value="">— seleccione —</option>
                  {cursos.map((c) => <option key={c.id} value={c.id}>{c.codigo} · {c.nombre}</option>)}
                </select>
              </div>
              <div className="field">
                <label>Estudiante</label>
                <select value={form.estudiante_id} disabled={!cursoSel}
                  onChange={(e) => setForm({ ...form, estudiante_id: e.target.value })}>
                  <option value="">
                    {cursoSel
                      ? (estudiantes.length ? "— seleccione —" : "Sin estudiantes matriculados")
                      : "Seleccione un curso primero"}
                  </option>
                  {estudiantes.map((e) => (
                    <option key={e.id} value={e.id}>{e.codigo} · {e.nombre_completo}</option>
                  ))}
                </select>
              </div>
              <div className="field">
                <label>Parcial 1</label>
                <input value={form.parcial1}
                  onChange={(e) => setForm({ ...form, parcial1: e.target.value })} />
              </div>
              <div className="field">
                <label>Parcial 2</label>
                <input value={form.parcial2}
                  onChange={(e) => setForm({ ...form, parcial2: e.target.value })} />
              </div>
              <div className="field">
                <label>Final</label>
                <input value={form.final}
                  onChange={(e) => setForm({ ...form, final: e.target.value })} />
              </div>
              <div className="field" style={{ display: "flex", alignItems: "flex-end" }}>
                <button className="btn btn-primary" onClick={registrar}>Guardar nota</button>
              </div>
            </div>
          </div>
        )}

        {rol === "admin" && (
          <div className="card mb-2">
            <div className="card-title">Consolidación de actas por curso</div>
            {consolidado.length === 0 ? (
              <div className="empty">Aún no hay actas registradas.</div>
            ) : (
              <table className="tabla">
                <thead>
                  <tr>
                    <th>Curso</th><th>Periodo</th><th>Notas</th><th>Validadas</th>
                    <th>Pendientes</th><th>Promedio</th><th>Estado</th><th></th>
                  </tr>
                </thead>
                <tbody>
                  {consolidado.map((c) => (
                    <tr key={`${c.curso_id}-${c.periodo}`}>
                      <td><b>{c.codigo}</b> {c.curso}</td>
                      <td>{c.periodo}</td>
                      <td>{c.total}</td>
                      <td>{c.validadas}</td>
                      <td>{c.pendientes}</td>
                      <td>{c.promedio}</td>
                      <td>{c.consolidada
                        ? <span className="badge badge-ok">Consolidada</span>
                        : <span className="badge badge-warn">Pendiente</span>}</td>
                      <td>{!c.consolidada &&
                        <button className="btn btn-primary btn-sm"
                          onClick={() => consolidar(c.curso_id, c.periodo)}>
                          Consolidar acta
                        </button>}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        )}

        <div className="card">
          <div className="card-title">Hoja de notas · 2026-I</div>
          {notas.length === 0 ? (
            <div className="empty">No hay notas registradas.</div>
          ) : (
            <table className="tabla">
              <thead>
                <tr>
                  {rol !== "estudiante" && <th>Estudiante</th>}
                  <th>Curso</th><th>P1</th><th>P2</th><th>Final</th>
                  <th>Promedio</th><th>Estado</th><th>Acta</th>
                  {rol === "admin" && <th></th>}
                </tr>
              </thead>
              <tbody>
                {notas.map((n) => (
                  <tr key={n.id}>
                    {rol !== "estudiante" && <td>{n.estudiante}</td>}
                    <td><b>{n.codigo}</b> {n.curso}</td>
                    <td>{n.parcial1 ?? "—"}</td>
                    <td>{n.parcial2 ?? "—"}</td>
                    <td>{n.final ?? "—"}</td>
                    <td><b>{n.promedio ?? "—"}</b></td>
                    <td><Badge estado={n.estado} /></td>
                    <td>{n.validada ? <span className="badge badge-ok">Validada</span>
                      : <span className="badge badge-warn">Pendiente</span>}</td>
                    {rol === "admin" && (
                      <td>{!n.validada &&
                        <button className="btn btn-primary btn-sm"
                          onClick={() => validar(n.id)}>Validar acta</button>}</td>
                    )}
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
