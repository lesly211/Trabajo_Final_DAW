import { useState, useEffect, useCallback, useRef } from 'react'
import { getApiUrl, logger } from '../config'
import './modules.css'

/**
 * MÓDULO 2: CURSOS Y DOCENTES — Olayne
 * - Asignación de docentes a cursos
 * - Gestión de horarios (detección de cruces)
 * - Carga de sílabos (PDF)
 */
const DIAS = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']

function CursosDocentes() {
  const [cursos, setCursos] = useState([])
  const [docentes, setDocentes] = useState([])
  const [msg, setMsg] = useState(null)
  const [horarioForm, setHorarioForm] = useState({ cursoId: null, dia: 'Lunes', hora_inicio: '08:00', hora_fin: '10:00', aula: '' })
  const fileInputs = useRef({})

  const cargar = useCallback(async () => {
    try {
      const [c, d] = await Promise.all([
        fetch(getApiUrl('/api/cursos')).then(r => r.json()),
        fetch(getApiUrl('/api/cursos/docentes')).then(r => r.json()),
      ])
      setCursos(c); setDocentes(d)
    } catch (err) {
      logger.error('Error cargando cursos/docentes', err)
    }
  }, [])

  useEffect(() => { cargar() }, [cargar])

  const notify = (tipo, texto) => setMsg({ tipo, texto })

  // ── Asignación de docentes ──
  const asignarDocente = async (cursoId, docenteId) => {
    try {
      const res = await fetch(getApiUrl(`/api/cursos/${cursoId}/docente`), {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ docente_id: docenteId ? Number(docenteId) : null })
      })
      const data = await res.json()
      if (!res.ok) return notify('error', data.error)
      notify('ok', docenteId
        ? `Docente asignado a ${data.codigo}: ${data.docente.nombre}`
        : `Se retiró el docente de ${data.codigo}`)
      cargar()
    } catch {
      notify('error', 'No se pudo conectar con el backend.')
    }
  }

  // ── Horarios ──
  const agregarHorario = async () => {
    const { cursoId, ...body } = horarioForm
    if (!body.aula.trim()) return notify('error', 'Indica el aula del bloque horario.')
    try {
      const res = await fetch(getApiUrl(`/api/cursos/${cursoId}/horarios`), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      })
      const data = await res.json()
      if (!res.ok) return notify('error', data.error)
      notify('ok', `Horario agregado a ${data.codigo}: ${body.dia} ${body.hora_inicio}–${body.hora_fin}`)
      setHorarioForm({ cursoId: null, dia: 'Lunes', hora_inicio: '08:00', hora_fin: '10:00', aula: '' })
      cargar()
    } catch {
      notify('error', 'No se pudo conectar con el backend.')
    }
  }

  const quitarHorario = async (cursoId, horarioId) => {
    const res = await fetch(getApiUrl(`/api/cursos/${cursoId}/horarios/${horarioId}`), { method: 'DELETE' })
    if (res.ok) { notify('ok', 'Bloque horario eliminado.'); cargar() }
  }

  // ── Sílabos ──
  const subirSilabo = async (cursoId, file) => {
    if (!file) return
    const fd = new FormData()
    fd.append('file', file)
    try {
      const res = await fetch(getApiUrl(`/api/cursos/${cursoId}/silabo`), { method: 'POST', body: fd })
      const data = await res.json()
      if (!res.ok) return notify('error', data.error)
      notify('ok', `Sílabo cargado para ${data.codigo}: ${data.silabo.nombre_archivo}`)
      cargar()
    } catch {
      notify('error', 'No se pudo conectar con el backend.')
    }
  }

  return (
    <div className="module-view">
      <div className="module-view-header">
        <h2>Cursos y Docentes</h2>
        <p>Asigna docentes, gestiona los horarios de cada curso y carga los sílabos del periodo.</p>
      </div>

      {msg && (
        <div className={`inline-msg ${msg.tipo}`} role="status">
          {msg.texto}
          <button className="msg-close" onClick={() => setMsg(null)} aria-label="Cerrar mensaje">×</button>
        </div>
      )}

      {/* ── Plana docente ── */}
      <section className="panel">
        <h3>Plana docente</h3>
        <div className="docentes-grid">
          {docentes.map(d => (
            <div key={d.id} className="docente-card">
              <strong>{d.nombre}</strong>
              <span>{d.grado} · {d.especialidad}</span>
              <span className={`carga ${d.cursos_asignados >= d.max_cursos ? 'llena' : ''}`}>
                Carga: {d.cursos_asignados}/{d.max_cursos} cursos
              </span>
            </div>
          ))}
        </div>
      </section>

      {/* ── Cursos ── */}
      <section className="panel">
        <h3>Cursos del periodo 2026-I</h3>
        {cursos.map(c => (
          <div key={c.id} className="curso-admin-card">
            <div className="curso-admin-head">
              <div>
                <span className="curso-code">{c.codigo}</span>
                <strong>{c.nombre}</strong>
                <span className="solicitud-meta">{c.creditos} créditos · Ciclo {c.ciclo}</span>
              </div>
              <select
                value={c.docente_id || ''}
                onChange={e => asignarDocente(c.id, e.target.value)}
                aria-label={`Docente de ${c.codigo}`}
                className={c.docente_id ? '' : 'sin-docente'}
              >
                <option value="">— Sin docente asignado —</option>
                {docentes.map(d => (
                  <option key={d.id} value={d.id}>{d.nombre}</option>
                ))}
              </select>
            </div>

            {/* Horarios */}
            <div className="horarios-block">
              <p className="field-label">Horarios</p>
              {c.horarios.length === 0
                ? <p className="empty-state">Sin bloques horarios definidos.</p>
                : (
                  <ul className="horario-list">
                    {c.horarios.map(h => (
                      <li key={h.id}>
                        <span>{h.dia} · {h.hora_inicio}–{h.hora_fin} · {h.aula}</span>
                        <button className="btn-ghost small" onClick={() => quitarHorario(c.id, h.id)}>Quitar</button>
                      </li>
                    ))}
                  </ul>
                )}

              {horarioForm.cursoId === c.id ? (
                <div className="horario-form">
                  <select value={horarioForm.dia} onChange={e => setHorarioForm(f => ({ ...f, dia: e.target.value }))} aria-label="Día">
                    {DIAS.map(d => <option key={d}>{d}</option>)}
                  </select>
                  <input type="time" value={horarioForm.hora_inicio} onChange={e => setHorarioForm(f => ({ ...f, hora_inicio: e.target.value }))} aria-label="Hora inicio" />
                  <input type="time" value={horarioForm.hora_fin} onChange={e => setHorarioForm(f => ({ ...f, hora_fin: e.target.value }))} aria-label="Hora fin" />
                  <input placeholder="Aula (ej. Lab A-301)" value={horarioForm.aula} onChange={e => setHorarioForm(f => ({ ...f, aula: e.target.value }))} />
                  <button className="btn-primary" onClick={agregarHorario}>Agregar</button>
                  <button className="btn-ghost" onClick={() => setHorarioForm(f => ({ ...f, cursoId: null }))}>Cancelar</button>
                </div>
              ) : (
                <button className="btn-ghost small" onClick={() => setHorarioForm(f => ({ ...f, cursoId: c.id }))}>
                  + Agregar bloque horario
                </button>
              )}
            </div>

            {/* Sílabo */}
            <div className="silabo-block">
              <p className="field-label">Sílabo</p>
              {c.silabo ? (
                <div className="silabo-info">
                  <span className="silabo-ok">📄 {c.silabo.nombre_archivo}</span>
                  <span className="solicitud-meta">Cargado el {c.silabo.fecha_carga} · {c.silabo.tamano_kb} KB</span>
                  <button className="btn-ghost small" onClick={() => fileInputs.current[c.id]?.click()}>Reemplazar</button>
                </div>
              ) : (
                <div className="silabo-info">
                  <span className="silabo-pendiente">Pendiente de carga</span>
                  <button className="btn-primary small" onClick={() => fileInputs.current[c.id]?.click()}>Cargar sílabo (PDF)</button>
                </div>
              )}
              <input
                type="file"
                accept="application/pdf"
                style={{ display: 'none' }}
                ref={el => { fileInputs.current[c.id] = el }}
                onChange={e => { subirSilabo(c.id, e.target.files[0]); e.target.value = '' }}
              />
            </div>
          </div>
        ))}
      </section>
    </div>
  )
}

export default CursosDocentes
