"""Application factory."""
from flask import Flask, jsonify
from .config import Config
from .extensions import db, jwt, cors


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Extensiones
    db.init_app(app)
    jwt.init_app(app)
    # El endpoint público de verificación de certificados y el resto de
    # rutas viven bajo /api/*; se restringe el origen al frontend
    # configurado en vez de aceptar cualquier origen ("*").
    cors.init_app(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})

    # Modelos (registro en metadata)
    from .models import (  # noqa: F401
        usuario, matricula, curso, nota, certificado, auditoria,
    )

    # Blueprints
    from .routes.auth_routes import auth_bp
    from .routes.matricula_routes import matricula_bp
    from .routes.curso_routes import curso_bp
    from .routes.nota_routes import nota_bp
    from .routes.record_routes import record_bp
    from .routes.certificado_routes import certificado_bp
    from .routes.seguridad_routes import seguridad_bp

    api = "/api"
    app.register_blueprint(auth_bp, url_prefix=f"{api}/auth")
    app.register_blueprint(matricula_bp, url_prefix=f"{api}/matricula")
    app.register_blueprint(curso_bp, url_prefix=f"{api}/cursos")
    app.register_blueprint(nota_bp, url_prefix=f"{api}/notas")
    app.register_blueprint(record_bp, url_prefix=f"{api}/record")
    app.register_blueprint(certificado_bp, url_prefix=f"{api}/certificados")
    app.register_blueprint(seguridad_bp, url_prefix=f"{api}")

    @app.get("/api/health")
    def health():
        return jsonify(status="ok", service="sistema-academico")

    @app.errorhandler(404)
    def not_found(e):
        return jsonify(error="Recurso no encontrado"), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify(error="Error interno del servidor"), 500

    return app
