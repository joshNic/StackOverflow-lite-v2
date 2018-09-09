from flask import jsonify, make_response

from app import create_app

app = create_app()
from .user_blueprint.user import mod
from .question_blueprint.question import qn_bp
from .answer_blueprint.answer import ans_bp
app.register_blueprint(mod, url_prefix='/api/v2/auth')
app.register_blueprint(qn_bp, url_prefix='/api/v2')
app.register_blueprint(ans_bp, url_prefix='/api/v2/question')


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Resource not found'}), 404)
