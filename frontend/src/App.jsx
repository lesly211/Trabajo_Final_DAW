import { useState, useEffect } from 'react'
import './App.css'
import config, { logger, getApiUrl } from './config'
import Matricula from './modules/Matricula'
import CursosDocentes from './modules/CursosDocentes'

function App() {
  const [vista, setVista] = useState('dashboard') // dashboard | matricula | cursos
  const [backendStatus, setBackendStatus] = useState('checking') // checking, connected, disconnected
  const [stats, setStats] = useState({
    students_count: 0,
    teachers_count: 0,
    courses_count: 0,
    faculties_count: 0
  })
  const [modules, setModules] = useState([])
  const [loading, setLoading] = useState(true)

  const checkBackend = async () => {
    setBackendStatus('checking')
    logger.log('Iniciando verificación de backend...')
    
    try {
      // 1. Check health
      const healthUrl = getApiUrl(config.API_ENDPOINTS.HEALTH)
      logger.log('Conectando a:', healthUrl)
      
      const healthRes = await fetch(healthUrl, { timeout: config.TIMEOUTS.API_REQUEST })
      const healthData = await healthRes.json()
      
      if (healthData.status === 'healthy') {
        setBackendStatus('connected')
        logger.log('Backend conectado exitosamente')
        
        // 2. Fetch stats
        const statsRes = await fetch(getApiUrl(config.API_ENDPOINTS.STATS))
        const statsData = await statsRes.json()
        setStats(statsData)
        logger.log('Estadísticas cargadas:', statsData)

        // 3. Fetch modules
        const modulesRes = await fetch(getApiUrl(config.API_ENDPOINTS.MODULES))
        const modulesData = await modulesRes.json()
        setModules(modulesData)
        logger.log('Módulos cargados:', modulesData)
      } else {
        setBackendStatus('disconnected')
        logger.warn('Backend respondió pero no está healthy')
      }
    } catch (error) {
      logger.error('Error conectando con backend', error)
      setBackendStatus('disconnected')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    checkBackend()
  }, [])

  return (
    <div className="dashboard-container">
      {/* Header */}
      <header className="dashboard-header">
        <div className="header-badge">Proyecto Académico Final</div>
        <h1>Sistema Académico Integral</h1>
        <p className="subtitle">
          Plataforma modular y escalable para la gestión de facultades, especialidades, matrícula y control académico.
        </p>
      </header>

      {/* Connection Status Banner */}
      <div className={`status-banner ${backendStatus}`}>
        <div className="status-indicator">
          <span className={`dot ${backendStatus}`}></span>
          <span className="status-text">
            {backendStatus === 'checking' && 'Verificando conexión con Flask Backend...'}
            {backendStatus === 'connected' && 'Servidor Backend Flask: Conectado online (Puerto 5000)'}
            {backendStatus === 'disconnected' && 'Servidor Backend Flask: Desconectado (Ejecuta el servidor Flask para conectar)'}
          </span>
        </div>
        <button className="btn-refresh" onClick={checkBackend} disabled={backendStatus === 'checking'}>
          {backendStatus === 'checking' ? 'Verificando...' : 'Reintentar Conexión'}
        </button>
      </div>

      {/* Navegación de módulos */}
      <nav className="app-nav" aria-label="Módulos del sistema">
        <button className={vista === 'dashboard' ? 'active' : ''} onClick={() => setVista('dashboard')}>Dashboard</button>
        <button className={vista === 'matricula' ? 'active' : ''} onClick={() => setVista('matricula')}>Matrícula</button>
        <button className={vista === 'cursos' ? 'active' : ''} onClick={() => setVista('cursos')}>Cursos y Docentes</button>
      </nav>

      {vista === 'matricula' && <Matricula />}
      {vista === 'cursos' && <CursosDocentes />}

      {vista === 'dashboard' && (<>
      {/* Stats Section */}
      <section className="stats-section">
        <div className="stat-card">
          <div className="stat-icon students">👥</div>
          <div className="stat-info">
            <h3>Estudiantes</h3>
            <p className="stat-value">{backendStatus === 'connected' ? stats.students_count : '--'}</p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon teachers">👨‍🏫</div>
          <div className="stat-info">
            <h3>Docentes</h3>
            <p className="stat-value">{backendStatus === 'connected' ? stats.teachers_count : '--'}</p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon courses">📚</div>
          <div className="stat-info">
            <h3>Cursos</h3>
            <p className="stat-value">{backendStatus === 'connected' ? stats.courses_count : '--'}</p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon faculties">🏛️</div>
          <div className="stat-info">
            <h3>Facultades</h3>
            <p className="stat-value">{backendStatus === 'connected' ? stats.faculties_count : '--'}</p>
          </div>
        </div>
      </section>

      {/* Modules Section */}
      <main className="modules-section">
        <div className="section-title">
          <h2>Módulos del Sistema</h2>
          <p>Estructura modular base configurada. Listos para ser desarrollados por el equipo.</p>
        </div>

        <div className="modules-grid">
          {backendStatus === 'connected' && modules.length > 0 ? (
            modules.map((mod) => (
              <div key={mod.id} className="module-card">
                <div className="module-header">
                  <span className={`module-badge ${mod.id}`}>Base Lista</span>
                  <div className="module-code">/api/{mod.id}</div>
                </div>
                <h3>{mod.name}</h3>
                <p>{mod.description}</p>
                <div className="module-footer">
                  <span className="dev-team">Estado: Listo para desarrollo</span>
                  <span className="arrow">→</span>
                </div>
              </div>
            ))
          ) : (
            // Fallback static modules if backend is not connected yet
            <>
              {[
                { id: 'matricula', name: 'Matrícula', desc: 'Gestión de inscripciones y matrículas de estudiantes.', icon: '📝' },
                { id: 'cursos', name: 'Cursos y Docentes', desc: 'Administración de asignaturas, horarios y asignación docente.', icon: '📖' },
                { id: 'notas', name: 'Control de Notas', desc: 'Registro y evaluación de calificaciones académicas.', icon: '📊' },
                { id: 'record', name: 'Récord Académico', desc: 'Historial académico y de progreso estudiantil.', icon: '🎓' },
                { id: 'documentos', name: 'Certificados y Documentos', desc: 'Emisión de constancias, certificados y trámites.', icon: '📁' },
                { id: 'seguridad', name: 'Administración y Seguridad', desc: 'Gestión de usuarios, roles diferenciados y auditoría.', icon: '🔒' }
              ].map((mod) => (
                <div key={mod.id} className="module-card fallback">
                  <div className="module-header">
                    <span className="module-icon-emoji">{mod.icon}</span>
                    <span className="module-badge status-offline">Offline</span>
                  </div>
                  <h3>{mod.name}</h3>
                  <p>{mod.desc}</p>
                  <div className="module-footer">
                    <span className="dev-team">Esperando conexión backend...</span>
                  </div>
                </div>
              ))}
            </>
          )}
        </div>
      </main>

      {/* Developer Instructions Footer */}
      <section className="instructions-section">
        <h3>Guía para el Equipo de Desarrollo</h3>
        <div className="instructions-grid">
          <div className="instruction-item">
            <div className="step-number">1</div>
            <h4>Frontend (React + Vite)</h4>
            <p>Trabajen dentro de <code>frontend/src/</code>. Pueden crear componentes en carpetas separadas para cada módulo.</p>
          </div>
          <div className="instruction-item">
            <div className="step-number">2</div>
            <h4>Backend (Flask API)</h4>
            <p>Agreguen sus controladores y rutas en <code>backend/app.py</code> o dividan en módulos dentro de <code>backend/</code>.</p>
          </div>
          <div className="instruction-item">
            <div className="step-number">3</div>
            <h4>Conexión CORS</h4>
            <p>El backend ya tiene CORS configurado para permitir peticiones desde cualquier origen de desarrollo.</p>
          </div>
        </div>
      </section>

      </>)}

      <footer className="main-footer">
        <p>Trabajo Final - Desarrollo de Aplicaciones Web © 2026</p>
      </footer>
    </div>
  )
}

export default App
