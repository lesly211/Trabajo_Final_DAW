import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [stats, setStats] = useState(null)
  const [modules, setModules] = useState([])
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(true)

  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        setError(null)

        // Fetch stats
        const statsResponse = await fetch(`${API_URL}/api/stats`)
        if (!statsResponse.ok) throw new Error('Failed to fetch stats')
        const statsData = await statsResponse.json()
        setStats(statsData)

        // Fetch modules
        const modulesResponse = await fetch(`${API_URL}/api/modules`)
        if (!modulesResponse.ok) throw new Error('Failed to fetch modules')
        const modulesData = await modulesResponse.json()
        setModules(modulesData)
      } catch (err) {
        setError(err.message)
        console.error('Error fetching data:', err)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  return (
    <div className="App">
      <header>
        <h1>📚 Sistema Académico</h1>
        <p>Plataforma de Gestión Académica Integral</p>
      </header>

      <main>
        {loading && (
          <section className="loading">
            <p>Cargando información del sistema...</p>
          </section>
        )}

        {error && (
          <section className="error">
            <p>❌ Error: {error}</p>
            <small>Asegúrese de que el servidor backend esté ejecutándose en {API_URL}</small>
          </section>
        )}

        {stats && !loading && (
          <>
            <section className="stats">
              <h2>Estadísticas del Sistema</h2>
              <div className="stats-grid">
                <div className="stat-card">
                  <div className="stat-number">{stats.students_count}</div>
                  <div className="stat-label">Estudiantes</div>
                </div>
                <div className="stat-card">
                  <div className="stat-number">{stats.teachers_count}</div>
                  <div className="stat-label">Docentes</div>
                </div>
                <div className="stat-card">
                  <div className="stat-number">{stats.courses_count}</div>
                  <div className="stat-label">Cursos</div>
                </div>
                <div className="stat-card">
                  <div className="stat-number">{stats.faculties_count}</div>
                  <div className="stat-label">Facultades</div>
                </div>
              </div>
            </section>

            {modules.length > 0 && (
              <section className="modules">
                <h2>Módulos Disponibles</h2>
                <div className="modules-grid">
                  {modules.map((module) => (
                    <div key={module.id} className="module-card">
                      <h3>{module.name}</h3>
                      <p>{module.description}</p>
                    </div>
                  ))}
                </div>
              </section>
            )}
          </>
        )}
      </main>

import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [stats, setStats] = useState(null)
  const [modules, setModules] = useState([])
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(true)

  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        setError(null)

        // Fetch stats
        const statsResponse = await fetch(`${API_URL}/api/stats`)
        if (!statsResponse.ok) throw new Error('Failed to fetch stats')
        const statsData = await statsResponse.json()
        setStats(statsData)

        // Fetch modules
        const modulesResponse = await fetch(`${API_URL}/api/modules`)
        if (!modulesResponse.ok) throw new Error('Failed to fetch modules')
        const modulesData = await modulesResponse.json()
        setModules(modulesData)
      } catch (err) {
        setError(err.message)
        console.error('Error fetching data:', err)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  return (
    <div className="App">
      <header>
        <h1>📚 Sistema Académico</h1>
        <p>Plataforma de Gestión Académica Integral</p>
      </header>

      <main>
        {loading && (
          <section className="loading">
            <p>Cargando información del sistema...</p>
          </section>
        )}

        {error && (
          <section className="error">
            <p>❌ Error: {error}</p>
            <small>Asegúrese de que el servidor backend esté ejecutándose en {API_URL}</small>
          </section>
        )}

        {stats && !loading && (
          <>
            <section className="stats">
              <h2>Estadísticas del Sistema</h2>
              <div className="stats-grid">
                <div className="stat-card">
                  <div className="stat-number">{stats.students_count}</div>
                  <div className="stat-label">Estudiantes</div>
                </div>
                <div className="stat-card">
                  <div className="stat-number">{stats.teachers_count}</div>
                  <div className="stat-label">Docentes</div>
                </div>
                <div className="stat-card">
                  <div className="stat-number">{stats.courses_count}</div>
                  <div className="stat-label">Cursos</div>
                </div>
                <div className="stat-card">
                  <div className="stat-number">{stats.faculties_count}</div>
                  <div className="stat-label">Facultades</div>
                </div>
              </div>
            </section>

            {modules.length > 0 && (
              <section className="modules">
                <h2>Módulos Disponibles</h2>
                <div className="modules-grid">
                  {modules.map((module) => (
                    <div key={module.id} className="module-card">
                      <h3>{module.name}</h3>
                      <p>{module.description}</p>
                    </div>
                  ))}
                </div>
              </section>
            )}
          </>
        )}
      </main>

      <footer>
        <p>© 2024 UNCP - Trabajo Final Desarrollo de Aplicaciones Web</p>
      </footer>
    </div>
  )
}

export default App
