import os
from flask import Flask, jsonify
from flask_cors import CORS
from config import get_config

# Load configuration
config = get_config()

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(config)

# Enable CORS with configuration
CORS(app, resources={r"/api/*": {"origins": config.CORS_ORIGINS}})

# Sample data to verify connection
ACADEMIC_STATS = {
    "students_count": 1250,
    "teachers_count": 85,
    "courses_count": 42,
    "faculties_count": 4
}

# Sample modules data
MODULES = [
    {"id": "matricula", "name": "Matrícula", "description": "Gestión de inscripciones y matrículas de estudiantes."},
    {"id": "cursos", "name": "Cursos y Docentes", "description": "Administración de asignaturas, horarios y asignación docente."},
    {"id": "notas", "name": "Control de Notas", "description": "Registro y evaluación de calificaciones académicas."},
    {"id": "record", "name": "Récord Académico", "description": "Historial académico y seguimiento de progreso estudiantil."},
    {"id": "documentos", "name": "Certificados y Documentos", "description": "Emisión de constancias, certificados y trámites documentales."},
    {"id": "seguridad", "name": "Administración y Seguridad", "description": "Gestión de usuarios, roles y auditoría del sistema."}
]

@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint to verify that the backend is running."""
    return jsonify({
        "status": "healthy",
        "message": "Backend Flask para el Sistema Académico está activo y funcionando.",
        "environment": config.FLASK_ENV,
        "version": config.API_VERSION
    }), 200

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Endpoint that returns basic statistics for the dashboard."""
    return jsonify(ACADEMIC_STATS), 200

@app.route('/api/modules', methods=['GET'])
def get_modules():
    """Endpoint listing the main modules of the academic system."""
    return jsonify(MODULES), 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "error": "Not Found",
        "message": "El endpoint solicitado no existe"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        "error": "Internal Server Error",
        "message": "Ha ocurrido un error interno en el servidor"
    }), 500

if __name__ == '__main__':
    # Get port from environment or default to 5000
    port = int(os.environ.get('PORT', 5000))
    debug_mode = config.DEBUG
    
    print(f"╔═══════════════════════════════════════════╗")
    print(f"║  {config.API_TITLE}")
    print(f"║  v{config.API_VERSION} - {config.FLASK_ENV.upper()}")
    print(f"║  Puerto: {port}")
    print(f"╚═══════════════════════════════════════════╝")
    # Run server
    app.run(host='0.0.0.0', port=port, debug=True)
