import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import PageHeader from "../components/PageHeader";
import Badge from "../components/Badge";
import Toast from "../components/Toast";
import { certificadoApi } from "../api/endpoints";

const TIPOS = ["Constancia de estudios", "Certificado de notas", "Constancia de egresado"];
const METODOS = [
  { value: "ambos", label: "QR + Firma digital" },
  { value: "qr", label: "Solo código QR" },
  { value: "firma_digital", label: "Solo firma digital" },
];

export default function Certificados() {
  const { usuario } = useAuth();
  const rol = usuario.rol;
  const [lista, setLista] = useState([]);
  const [tipo, setTipo] = useState(TIPOS[0]);
  const [metodos, setMetodos] = useState({}); // método elegido por certificado (admin)
  const [toast, setToast] = useState("");

  const cargar = () => certificadoApi.listar().then((r) => setLista(r.data));
  useEffect(() => { cargar(); }, []);

  const solicitar = async () => {
    await certificadoApi.solicitar({ tipo });
    setToast("Solicitud enviada.");
    cargar();
  };
  const autorizar = async (id) => {
    await certificadoApi.autorizar(id);
    setToast("Documento autorizado.");
    cargar();
  };
  const emitir = async (id) => {
    try {
      const metodo = metodos[id] || "ambos";
      await certificadoApi.emitir(id, metodo);
      setToast("Certificado emitido.");
    } catch (e) {
      setToast(e.response?.data?.error || "Error al emitir.");
    }
    cargar();
  };
  const descargarPdf = async (id) => {
    try {
      const r = await certificadoApi.descargarPdf(id);
      const url = window.URL.createObjectURL(new Blob([r.data], { type: "application/pdf" }));
      const a = document.createElement("a");
      a.href = url;
      a.download = `certificado_${id}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch {
      setToast("No se pudo descargar el documento.");
    }
  };

  return (
    <>
      <PageHeader tag="Módulo 5" title={
        rol === "estudiante" ? "Certificados y Documentos"
          : rol === "direccion" ? "Autorización de Documentos" : "Emisión de Certificados"
      } subtitle={
        rol === "estudiante" ? "Solicite certificados y constancias en línea."
          : rol === "direccion" ? "Autorice la emisión de documentos oficiales."
          : "Emita certificados con firma digital y/o código QR de verificación."
      } />
      <div className="content">
        {rol === "estudiante" && (
          <div className="card mb-2">
            <div className="card-title">Solicitar documento</div>
            <div className="row">
              <select className="field" style={{ margin: 0, minWidth: 260 }}
                value={tipo} onChange={(e) => setTipo(e.target.value)}>
                {TIPOS.map((t) => <option key={t}>{t}</option>)}
              </select>
              <button className="btn btn-primary" onClick={solicitar}>Solicitar</button>
            </div>
          </div>
        )}

        <div className="card">
          <div className="card-title">Documentos</div>
          {lista.length === 0 ? <div className="empty">Sin documentos.</div> : (
            <table className="tabla">
              <thead>
                <tr>
                  {rol !== "estudiante" && <th>Estudiante</th>}
                  <th>Tipo</th><th>Estado</th><th>Autorizado</th>
                  <th>Código</th><th>QR</th><th>Firma digital</th><th></th>
                </tr>
              </thead>
              <tbody>
                {lista.map((c) => (
                  <tr key={c.id}>
                    {rol !== "estudiante" && <td>{c.estudiante}</td>}
                    <td>{c.tipo}</td>
                    <td><Badge estado={c.estado} /></td>
                    <td>{c.autorizado ? <span className="badge badge-ok">Sí</span>
                      : <span className="badge badge-warn">No</span>}</td>
                    <td>{c.codigo_verificacion || "—"}</td>
                    <td>{c.qr_base64 ? <img className="qr-img" src={c.qr_base64} alt="QR" /> : "—"}</td>
                    <td>
                      {c.firma_digital
                        ? <code title={c.firma_digital}>{c.firma_digital.slice(0, 10)}…</code>
                        : "—"}
                    </td>
                    <td>
                      <div className="row" style={{ gap: 6, flexWrap: "wrap" }}>
                        {rol === "direccion" && !c.autorizado &&
                          <button className="btn btn-primary btn-sm"
                            onClick={() => autorizar(c.id)}>Autorizar</button>}

                        {rol === "admin" && c.estado === "solicitado" && c.autorizado && (
                          <>
                            <select
                              value={metodos[c.id] || "ambos"}
                              onChange={(e) => setMetodos({ ...metodos, [c.id]: e.target.value })}
                              style={{ minWidth: 170 }}>
                              {METODOS.map((m) => <option key={m.value} value={m.value}>{m.label}</option>)}
                            </select>
                            <button className="btn btn-gold btn-sm" onClick={() => emitir(c.id)}>
                              Emitir
                            </button>
                          </>
                        )}
                        {rol === "admin" && c.estado === "solicitado" && !c.autorizado &&
                          <span className="muted">Esperando autorización de Dirección</span>}

                        {c.estado === "emitido" && (
                          <>
                            <button className="btn btn-sm" onClick={() => descargarPdf(c.id)}>
                              Descargar PDF
                            </button>
                            <a className="btn btn-outline btn-sm"
                              href={`/verificar/${c.codigo_verificacion}`}
                              target="_blank" rel="noreferrer">
                              Ver verificación
                            </a>
                          </>
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
