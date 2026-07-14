import { useState, useEffect, useCallback } from 'react'
import { getApiUrl, logger } from '../config'
import './modules.css'

/**
 * MÓDULO 1: MATRÍCULA — Olayne
 * - Solicitud de matrícula con validación de requisitos
 * - Registro de pagos
 * - Ficha oficial de matrícula
 */
function Matricula() {
  const [estudiantes, setEstudiantes] = useState([])
  const [cursos, setCursos] = useState([])
  const [solicitudes, setSolicitudes] = useState([])

  // Formulario nueva solicitud
  const [estudianteId, setEstudianteId] = useState('')
  const [cursosSel, setCursosSel] = useState([])
  const [enviando, setEnviando] = useState(false)
  const [msg, setMsg] = useState(null) // {tipo: 'ok'|'error', texto}

  // Pago
  const [pagoForm, setPagoForm] = useState({ solicitudId: null, metodo: 'Yape/Plin', nro_operacion: '' })

  // Ficha visible
  const [fichaVisible, setFichaVisible] = useState(null)

  const cargar = useCallback(async () => {
    try {
      const [e, c, s] = await Promise.all([
        fetch(getApiUrl('/api/matricula/estudiantes')).then(r => r.json()),
        fetch(getApiUrl('/api/cursos')).then(r => r.json()),
        fetch(getApiUrl('/api/matricula/solicitudes')).then(r => r.json()),
      ])
      setEstudiantes(e); setCursos(c); setSolicitudes(s)
    } catch (err) {
      logger.error('Error cargando datos de matrícula', err)
    }
  }, [])

  useEffect(() => { cargar() }, [cargar])

  const toggleCurso = (id) => {
    setCursosSel(prev => prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id])
  }

  const creditosSel = cursos.filter(c => cursosSel.includes(c.id)).reduce((a, c) => a + c.creditos, 0)

  const crearSolicitud = async () => {
    if (!estudianteId || cursosSel.length === 0) {
      setMsg({ tipo: 'error', texto: 'Selecciona un estudiante y al menos un curso.' })
      return
    }
    setEnviando(true); setMsg(null)
    try {
      const res = await fetch(getApiUrl('/api/matricula/solicitudes'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ estudiante_id: Number(estudianteId), cursos_ids: cursosSel })
      })
      const data = await res.json()
      if (!res.ok) {
        setMsg({ tipo: 'error', texto: data.error })
      } else {
        setMsg({
          tipo: data.estado === 'observada' ? 'error' : 'ok',
          texto: data.estado === 'observada'
            ? `Solicitud ${data.numero} registrada como OBSERVADA: revisa los requisitos incumplidos.`
            : `Solicitud ${data.numero} validada. Pasa a registrar el pago (S/ ${data.monto_total.toFixed(2)}).`
        })
        setEstudianteId(''); setCursosSel([])
        cargar()
      }
    } catch {
      setMsg({ tipo: 'error', texto: 'No se pudo conectar con el backend.' })
    } finally {
      setEnviando(false)
    }
  }

  const registrarPago = async (sol) => {
    if (!pagoForm.nro_operacion.trim()) {
      setMsg({ tipo: 'error', texto: 'Ingresa el número de operación del pago.' })
      return
    }
    try {
      const res = await fetch(getApiUrl(`/api/matricula/solicitudes/${sol.id}/pago`), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ metodo: pagoForm.metodo, nro_operacion: pagoForm.nro_operacion, monto: sol.monto_total })
      })
      const data = await res.json()
      if (!res.ok) {
        setMsg({ tipo: 'error', texto: data.error })
      } else {
        setMsg({ tipo: 'ok', texto: `Pago registrado. Ficha oficial generada: ${data.ficha.numero}` })
        setPagoForm({ solicitudId: null, metodo: 'Yape/Plin', nro_operacion: '' })
        setFichaVisible(data)
        cargar()
      }
    } catch {
      setMsg({ tipo: 'error', texto: 'No se pudo conectar con el backend.' })
    }
  }

  const verFicha = async (sol) => {
    const res = await fetch(getApiUrl(`/api/matricula/solicitudes/${sol.id}/ficha`))
    const data = await res.json()
    if (res.ok) setFichaVisible(data)
    else setMsg({ tipo: 'error', texto: data.error })
  }

  const estadoLabel = { observada: 'Observada', pendiente_pago: 'Pendiente de pago', matriculado: 'Matriculado' }

  return (
    <div className="module-view">
      <div className="module-view-header">
        <h2>Módulo de Matrícula</h2>
        <p>Registra solicitudes, valida requisitos, confirma pagos y emite la ficha oficial.</p>
      </div>

      {msg && (
        <div className={`inline-msg ${msg.tipo}`} role="status">
          {msg.texto}
          <button className="msg-close" onClick={() => setMsg(null)} aria-label="Cerrar mensaje">×</button>
        </div>
      )}

      {/* ── Nueva solicitud ── */}
      <section className="panel">
        <h3>Nueva solicitud de matrícula</h3>
        <div className="form-row">
          <label htmlFor="sel-est">Estudiante</label>
          <select id="sel-est" value={estudianteId} onChange={e => setEstudianteId(e.target.value)}>
            <option value="">— Seleccionar estudiante —</option>
            {estudiantes.map(e => (
              <option key={e.id} value={e.id}>{e.codigo} · {e.nombre}</option>
            ))}
          </select>
        </div>

        <p className="field-label">Cursos del periodo 2026-I</p>
        <div className="curso-picker">
          {cursos.map(c => (
            <label key={c.id} className={`curso-check ${cursosSel.includes(c.id) ? 'checked' : ''}`}>
              <input
                type="checkbox"
                checked={cursosSel.includes(c.id)}
                onChange={() => toggleCurso(c.id)}
              />
              <span className="curso-code">{c.codigo}</span>
              <span className="curso-name">{c.nombre}</span>
              <span className="curso-cred">{c.creditos} cr.</span>
            </label>
          ))}
        </div>

        <div className="picker-footer">
          <span>Créditos seleccionados: <strong>{creditosSel}</strong> / 22 &nbsp;·&nbsp; Costo estimado: <strong>S/ {(creditosSel * 85).toFixed(2)}</strong></span>
          <button className="btn-primary" onClick={crearSolicitud} disabled={enviando}>
            {enviando ? 'Validando requisitos...' : 'Registrar y validar solicitud'}
          </button>
        </div>
      </section>

      {/* ── Solicitudes ── */}
      <section className="panel">
        <h3>Solicitudes registradas</h3>
        {solicitudes.length === 0 ? (
          <p className="empty-state">Aún no hay solicitudes. Crea la primera con el formulario superior.</p>
        ) : (
          solicitudes.map(s => (
            <div key={s.id} className={`solicitud-card ${s.estado}`}>
              <div className="solicitud-head">
                <div>
                  <span className="solicitud-num">{s.numero}</span>
                  <strong>{s.estudiante.nombre}</strong>
                  <span className="solicitud-meta">{s.estudiante.codigo} · {s.periodo} · {s.creditos_total} créditos · S/ {s.monto_total.toFixed(2)}</span>
                </div>
                <span className={`estado-badge ${s.estado}`}>{estadoLabel[s.estado]}</span>
              </div>

              {/* Validación de requisitos */}
              <details className="req-details" open={s.estado === 'observada'}>
                <summary>Validación de requisitos {s.validacion.apto ? '· Apto ✔' : '· Con observaciones'}</summary>
                <ul className="req-list">
                  {s.validacion.checks.map(ch => (
                    <li key={ch.codigo} className={ch.cumple ? 'ok' : 'fail'}>
                      <span className="req-mark">{ch.cumple ? '✔' : '✕'}</span> {ch.descripcion}
                    </li>
                  ))}
                </ul>
              </details>

              {/* Registro de pago */}
              {s.estado === 'pendiente_pago' && (
                pagoForm.solicitudId === s.id ? (
                  <div className="pago-form">
                    <select
                      value={pagoForm.metodo}
                      onChange={e => setPagoForm(p => ({ ...p, metodo: e.target.value }))}
                      aria-label="Método de pago"
                    >
                      <option>Yape/Plin</option>
                      <option>Efectivo</option>
                      <option>Tarjeta</option>
                      <option>Transferencia</option>
                    </select>
                    <input
                      placeholder="N.º de operación"
                      value={pagoForm.nro_operacion}
                      onChange={e => setPagoForm(p => ({ ...p, nro_operacion: e.target.value }))}
                    />
                    <span className="pago-monto">S/ {s.monto_total.toFixed(2)}</span>
                    <button className="btn-primary" onClick={() => registrarPago(s)}>Confirmar pago</button>
                    <button className="btn-ghost" onClick={() => setPagoForm({ solicitudId: null, metodo: 'Yape/Plin', nro_operacion: '' })}>Cancelar</button>
                  </div>
                ) : (
                  <button className="btn-primary" onClick={() => setPagoForm({ solicitudId: s.id, metodo: 'Yape/Plin', nro_operacion: '' })}>
                    Registrar pago
                  </button>
                )
              )}

              {s.estado === 'matriculado' && (
                <div className="ficha-row">
                  <span>Ficha oficial: <strong>{s.ficha.numero}</strong> · Pago {s.pago.metodo} ({s.pago.nro_operacion})</span>
                  <button className="btn-ghost" onClick={() => verFicha(s)}>Ver ficha oficial</button>
                </div>
              )}
            </div>
          ))
        )}
      </section>

      {/* ── Ficha oficial (modal imprimible) ── */}
      {fichaVisible && (
        <div className="modal-overlay" onClick={() => setFichaVisible(null)}>
          <div className="ficha-oficial" onClick={e => e.stopPropagation()}>
            <header className="ficha-head">
              <div>
                <h3>Ficha oficial de matrícula</h3>
                <p>Sistema Académico Integral · Periodo {fichaVisible.periodo}</p>
              </div>
              <div className="ficha-num">
                <span>{fichaVisible.ficha.numero}</span>
                <small>Emitida: {fichaVisible.ficha.fecha_emision}</small>
              </div>
            </header>

            <div className="ficha-datos">
              <div><small>Estudiante</small><strong>{fichaVisible.estudiante.nombre}</strong></div>
              <div><small>Código</small><strong>{fichaVisible.estudiante.codigo}</strong></div>
              <div><small>Carrera</small><strong>{fichaVisible.estudiante.carrera}</strong></div>
              <div><small>Ciclo</small><strong>{fichaVisible.estudiante.ciclo}</strong></div>
            </div>

            <table className="ficha-tabla">
              <thead>
                <tr><th>Código</th><th>Curso</th><th>Cr.</th><th>Docente</th><th>Horario</th></tr>
              </thead>
              <tbody>
                {fichaVisible.cursos.map(c => (
                  <tr key={c.id}>
                    <td>{c.codigo}</td>
                    <td>{c.nombre}</td>
                    <td>{c.creditos}</td>
                    <td>{c.docente}</td>
                    <td>{c.horarios.map(h => `${h.dia} ${h.hora_inicio}–${h.hora_fin} (${h.aula})`).join(' · ') || '—'}</td>
                  </tr>
                ))}
              </tbody>
              <tfoot>
                <tr>
                  <td colSpan="2"><strong>Total</strong></td>
                  <td><strong>{fichaVisible.creditos_total}</strong></td>
                  <td colSpan="2"><strong>Pagado: S/ {fichaVisible.monto_total.toFixed(2)} · {fichaVisible.pago.metodo} · Op. {fichaVisible.pago.nro_operacion}</strong></td>
                </tr>
              </tfoot>
            </table>

            <footer className="ficha-foot">
              <span className="sello">MATRICULADO</span>
              <div className="ficha-actions">
                <button className="btn-primary" onClick={() => window.print()}>Imprimir</button>
                <button className="btn-ghost" onClick={() => setFichaVisible(null)}>Cerrar</button>
              </div>
            </footer>
          </div>
        </div>
      )}
    </div>
  )
}

export default Matricula
