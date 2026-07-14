import { useEffect, useState } from "react";
import PageHeader from "../components/PageHeader";
import Toast from "../components/Toast";
import { seguridadApi } from "../api/endpoints";
import { rolLabel } from "../utils/format";

const ROLES = ["estudiante", "docente", "admin", "direccion"];

export default function Usuarios() {
  const [lista, setLista] = useState([]);
  const [toast, setToast] = useState("");
  const [form, setForm] = useState({
    username: "", nombres: "", apellidos: "", rol: "estudiante",
    codigo: "", especialidad: "Ingeniería de Sistemas", password: "123456",
  });

  const cargar = () => seguridadApi.usuarios().then((r) => setLista(r.data));
  useEffect(() => { cargar(); }, []);

  const crear = async () => {
    try {
      await seguridadApi.crearUsuario(form);
      setToast("Usuario creado.");
      setForm({ ...form, username: "", nombres: "", apellidos: "", codigo: "" });
      cargar();
    } catch (e) {
      setToast(e.response?.data?.error || "Error al crear usuario.");
    }
  };

  const toggleActivo = async (u) => {
    await seguridadApi.actualizarUsuario(u.id, { activo: !u.activo });
    cargar();
  };

  return (
    <>
      <PageHeader tag="Módulo 6" title="Administración y Seguridad"
        subtitle="Defina perfiles de acceso y gestione los usuarios del sistema." />
      <div className="content">
        <div className="card mb-2">
          <div className="card-title">Nuevo usuario</div>
          <div className="grid grid-3">
            <div className="field"><label>Usuario</label>
              <input value={form.username} onChange={(e) => setForm({ ...form, username: e.target.value })} /></div>
            <div className="field"><label>Nombres</label>
              <input value={form.nombres} onChange={(e) => setForm({ ...form, nombres: e.target.value })} /></div>
            <div className="field"><label>Apellidos</label>
              <input value={form.apellidos} onChange={(e) => setForm({ ...form, apellidos: e.target.value })} /></div>
            <div className="field"><label>Rol</label>
              <select value={form.rol} onChange={(e) => setForm({ ...form, rol: e.target.value })}>
                {ROLES.map((r) => <option key={r} value={r}>{rolLabel[r]}</option>)}
              </select></div>
            <div className="field"><label>Código</label>
              <input value={form.codigo} onChange={(e) => setForm({ ...form, codigo: e.target.value })} /></div>
            <div className="field" style={{ display: "flex", alignItems: "flex-end" }}>
              <button className="btn btn-primary" onClick={crear}>Crear usuario</button>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="card-title">Usuarios registrados ({lista.length})</div>
          <table className="tabla">
            <thead><tr><th>Usuario</th><th>Nombre</th><th>Rol</th>
              <th>Código</th><th>Estado</th><th></th></tr></thead>
            <tbody>
              {lista.map((u) => (
                <tr key={u.id}>
                  <td>{u.username}</td>
                  <td>{u.nombre_completo}</td>
                  <td><span className="badge badge-neutral">{rolLabel[u.rol]}</span></td>
                  <td>{u.codigo || "—"}</td>
                  <td>{u.activo ? <span className="badge badge-ok">Activo</span>
                    : <span className="badge badge-danger">Inactivo</span>}</td>
                  <td>
                    <button className="btn btn-outline btn-sm" onClick={() => toggleActivo(u)}>
                      {u.activo ? "Desactivar" : "Activar"}
                    </button>
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
