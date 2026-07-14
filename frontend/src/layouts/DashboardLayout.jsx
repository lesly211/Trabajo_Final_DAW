import { NavLink, Outlet } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { rolLabel } from "../utils/format";

// Menú por rol
const MENU = {
  estudiante: [
    ["/", "Inicio"],
    ["/matricula", "Matrícula"],
    ["/notas", "Mis Notas"],
    ["/record", "Record Académico"],
    ["/certificados", "Certificados"],
  ],
  docente: [
    ["/", "Inicio"],
    ["/cursos", "Mis Cursos"],
    ["/notas", "Registro de Notas"],
  ],
  admin: [
    ["/", "Inicio"],
    ["/matricula", "Matrículas"],
    ["/cursos", "Cursos y Docentes"],
    ["/notas", "Actas"],
    ["/certificados", "Certificados"],
    ["/usuarios", "Usuarios"],
  ],
  direccion: [
    ["/", "Inicio"],
    ["/cursos", "Carga Docente"],
    ["/certificados", "Autorizaciones"],
    ["/auditoria", "Auditoría"],
  ],
};

export default function DashboardLayout() {
  const { usuario, logout } = useAuth();
  const items = MENU[usuario.rol] || [];

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="sidebar-brand">
          <span>FIS · UNCP</span>
          <h1>Sistema Académico</h1>
        </div>
        <nav className="nav-section">
          {items.map(([to, label]) => (
            <NavLink key={to} to={to} end={to === "/"}
              className={({ isActive }) => "nav-link" + (isActive ? " active" : "")}>
              <span className="dot" />
              <span>{label}</span>
            </NavLink>
          ))}
        </nav>
        <div className="sidebar-user">
          <small>{rolLabel[usuario.rol]}</small>
          <b>{usuario.nombre_completo}</b>
          <button className="btn-logout" onClick={logout}>Cerrar sesión</button>
        </div>
      </aside>
      <main className="main">
        <Outlet />
      </main>
    </div>
  );
}
