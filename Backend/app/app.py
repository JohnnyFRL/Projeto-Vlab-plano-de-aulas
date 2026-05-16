import os
from flask import Flask
from dotenv import load_dotenv

from app.extensions import db, cors
from app.config.settings import config_by_env
from app.routes.lesson_plan_routes import lesson_plan_bp
from app.routes.health_routes import health_bp

load_dotenv()


def create_app():
    app = Flask(__name__)

    env = os.getenv("FLASK_ENV", "development")
    app.config.from_object(config_by_env.get(env, config_by_env["development"]))

    db.init_app(app)
    cors.init_app(app)

    app.register_blueprint(lesson_plan_bp)
    app.register_blueprint(health_bp)

    with app.app_context():
        db.create_all()

    return app
