import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Enable CORS for all routes, allowing requests from our React frontend
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Sample data to verify connection
ACADEMIC_STATS = {
    "students_count": 1250,
    "teachers_count": 85,
    "courses_count": 42,
    "faculties_count": 4
}

@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint to verify that the backend is running."""
    return jsonify({
        "status": "healthy",
        "message": "Backend Flask para el Sistema Académico está activo y funcionando."
    }), 200

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Endpoint that returns basic statistics for the dashboard."""
    return jsonify(ACADEMIC_STATS), 200

@app.route('/api/modules', methods=['GET'])
def get_modules():
    """Endpoint listing the main modules of the academic system."""
    modules = [
        {"id": "matricula", "name": "Matrícula", "description": "Gestión de inscripciones y matrículas de estudiantes."},
        {"id": "cursos", "name": "Cursos y Docentes", "description": "Administración de asignaturas, horarios y asignación docente."},
        {"id": "notas", "name": "Control de Notas", "description": "Registro y evaluación de calificaciones académicas."},
        {"id": "record", "name": "Récord Académico", "description": "Historial académico y seguimiento de progreso estudiantil."},
        {"id": "documentos", "name": "Certificados y Documentos", "description": "Emisión de constancias, certificados y trámites documentales."},
        {"id": "seguridad", "name": "Administración y Seguridad", "description": "Gestión de usuarios, roles y auditoría del sistema."}
    ]
    return jsonify(modules), 200

if __name__ == '__main__':
    # Get port from environment or default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Run server
    app.run(host='0.0.0.0', port=port, debug=True)
