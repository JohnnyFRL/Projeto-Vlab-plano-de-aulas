import os
from flask import Flask
from dotenv import load_dotenv

from app.extensions import db, cors
from app.config.settings import config_by_env
from app.utils.logger import setup_logging
from app.utils.error_handlers import register_error_handlers

load_dotenv()


def create_app():
    setup_logging()

    app = Flask(__name__)

    env = os.getenv("FLASK_ENV", "development")
    app.config.from_object(config_by_env.get(env, config_by_env["development"]))

    db.init_app(app)
    cors.init_app(app)

    from app.routes.lesson_plan_routes import lesson_plan_bp
    from app.routes.health_routes import health_bp

    app.register_blueprint(lesson_plan_bp)
    app.register_blueprint(health_bp)

    register_error_handlers(app)

    with app.app_context():
        from app.models import lesson_plan  # noqa: F401
        db.create_all()

    return app
