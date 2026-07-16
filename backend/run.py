"""Punto de entrada de la aplicación."""
import os
from dotenv import load_dotenv

load_dotenv()

from app import create_app
from app.extensions import db
from app.seeds.seed_data import seed_all

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed_all()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
