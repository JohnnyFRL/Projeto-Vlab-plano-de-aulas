from flask import jsonify
from marshmallow import ValidationError
from app.utils.logger import get_logger

logger = get_logger(__name__)


def register_error_handlers(app):

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"error": "Requisição inválida."}), 400

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Recurso não encontrado."}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"error": "Método não permitido."}), 405

    @app.errorhandler(ValidationError)
    def validation_error(e):
        return jsonify({"error": "Dados inválidos.", "details": e.messages}), 400

    @app.errorhandler(Exception)
    def unhandled_exception(e):
        logger.error("Erro interno não tratado: %s", str(e), exc_info=True)
        return jsonify({"error": "Erro interno no servidor."}), 500
