import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [identifier, setIdentifier] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [cargando, setCargando] = useState(false);

  const onSubmit = async () => {
    setError("");
    setCargando(true);
    try {
      await login(identifier, password);
      navigate("/");
    } catch {
      setError("Código o contraseña incorrectos.");
    } finally {
      setCargando(false);
    }
  };

  return (
    <div className="login-wrap">
      <div className="login-art">
        <span className="eyebrow">Facultad de Ingeniería de Sistemas</span>
        <h1>Gestión académica integral, segura y en línea.</h1>
      </div>
      <div className="login-form-wrap">
        <div className="login-card">
          <h2>Iniciar sesión</h2>
          <p className="sub">Acceda con sus credenciales institucionales.</p>
          {error && <div className="login-error">{error}</div>}
          <div className="field">
            <label>Código / Usuario</label>
            <input value={identifier} onChange={(e) => setIdentifier(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && onSubmit()}
              placeholder="ej. 2021100123 · d-marialopez001 · a-001" />
          </div>
          <div className="field">
            <label>Contraseña</label>
            <input type="password" value={password}
              onChange={(e) => setPassword(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && onSubmit()}
              placeholder="••••••" />
          </div>
          <button className="btn btn-primary" style={{ width: "100%" }}
            onClick={onSubmit} disabled={cargando}>
            {cargando ? "Ingresando…" : "Ingresar"}
          </button>
        </div>
      </div>
    </div>
  );
}
