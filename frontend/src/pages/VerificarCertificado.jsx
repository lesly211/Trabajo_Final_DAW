import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { certificadoApi } from "../api/endpoints";

const METODO_LABEL = {
  qr: "Código QR",
  firma_digital: "Firma digital (HMAC-SHA256)",
  ambos: "Código QR + Firma digital",
};

/**
 * Página pública (sin autenticación) a la que apunta el código QR impreso
 * en cada certificado emitido. Permite a cualquier persona (por ejemplo,
 * una entidad externa) verificar la autenticidad de un documento sin
 * necesidad de iniciar sesión en el sistema.
 */
export default function VerificarCertificado() {
  const { codigo } = useParams();
  const [estado, setEstado] = useState("cargando"); // cargando | ok | error
  const [data, setData] = useState(null);
  const [mensaje, setMensaje] = useState("");

  useEffect(() => {
    certificadoApi
      .verificar(codigo)
      .then((r) => {
        setData(r.data);
        setEstado("ok");
      })
      .catch((e) => {
        setMensaje(e.response?.data?.mensaje || "No se pudo verificar el documento.");
        setEstado("error");
      });
  }, [codigo]);

  const valido = estado === "ok" && data?.valido && data?.firma_integra !== false;

  return (
    <div className="login-wrap">
      <div className="login-art">
        <span className="eyebrow">Verificación pública de documentos</span>
        <h1>Sistema Académico Integral — FIS UNCP</h1>
        <p>
          Esta página confirma, sin necesidad de iniciar sesión, si un
          certificado o constancia emitido por la Facultad de Ingeniería de
          Sistemas es auténtico y no ha sido alterado.
        </p>
      </div>
      <div className="login-form-wrap">
        <div className="login-card">
          {estado === "cargando" && <div className="empty">Verificando código…</div>}

          {estado === "error" && (
            <>
              <div className="section-tag" style={{ color: "var(--danger)" }}>
                Documento no válido
              </div>
              <h2 style={{ color: "var(--danger)" }}>No se pudo verificar</h2>
              <div className="login-error">{mensaje}</div>
              <p className="muted">
                Código consultado: <code>{codigo}</code>
              </p>
            </>
          )}

          {estado === "ok" && (
            <>
              <div
                className="section-tag"
                style={{ color: valido ? "var(--ok)" : "var(--danger)" }}
              >
                {valido ? "Documento auténtico" : "Integridad no verificada"}
              </div>
              <h2 style={{ color: valido ? "var(--verde-900)" : "var(--danger)" }}>
                {valido ? "✓ Certificado válido" : "⚠ Firma no coincide"}
              </h2>
              <p className="sub">
                {valido
                  ? "Este documento fue emitido oficialmente por el sistema y su contenido no ha sido alterado."
                  : "El código existe, pero la firma digital no coincide con los datos del documento."}
              </p>

              <div className="card" style={{ boxShadow: "none", border: "1px solid var(--gris-300)", marginTop: 16 }}>
                <div className="field">
                  <label>Tipo de documento</label>
                  <div><b>{data.tipo}</b></div>
                </div>
                <div className="field">
                  <label>Emitido a</label>
                  <div>{data.estudiante || "—"}</div>
                </div>
                <div className="field">
                  <label>Código de verificación</label>
                  <div><code>{data.codigo_verificacion}</code></div>
                </div>
                <div className="field">
                  <label>Método de emisión</label>
                  <div>{METODO_LABEL[data.metodo_emision] || data.metodo_emision || "—"}</div>
                </div>
                <div className="field" style={{ marginBottom: 0 }}>
                  <label>Fecha de emisión</label>
                  <div>{data.emitido_en || "—"}</div>
                </div>
              </div>
            </>
          )}

          <div className="login-hint">
            <Link to="/login">Volver al inicio de sesión</Link>
          </div>
        </div>
      </div>
    </div>
  );
}
