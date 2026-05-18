import os
import logging
from flask import Flask, jsonify
from dotenv import load_dotenv

from app.extensions import db, cors
from app.config.settings import config_by_env

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)


def create_app():
    app = Flask(__name__)

    env = os.getenv("FLASK_ENV", "development")
    app.config.from_object(config_by_env.get(env, config_by_env["development"]))

    db.init_app(app)
    cors.init_app(app)

    from app.routes.lesson_plan_routes import lesson_plan_bp
    from app.routes.health_routes import health_bp

    app.register_blueprint(lesson_plan_bp)
    app.register_blueprint(health_bp)

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Recurso não encontrado."}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "Erro interno no servidor."}), 500

    with app.app_context():
        from app.models import lesson_plan  # noqa: F401
        db.create_all()

    return app
