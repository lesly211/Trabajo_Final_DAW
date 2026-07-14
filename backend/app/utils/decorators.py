"""Decoradores de autorización por rol."""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt


def roles_required(*roles):
    """Permite el acceso solo a los roles indicados."""
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get("rol") not in roles:
                return jsonify(error="No autorizado para este recurso"), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper
