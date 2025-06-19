from flask import jsonify, Blueprint, make_response, request
from werkzeug.exceptions import NotFound

from data import db_session
from data.users import User

users_bp = Blueprint('users_api', __name__, template_folder='templates')


@users_bp.route('/users', methods=['GET'])
def post_login(**args):
    with db_session.create_session() as session:
        user = session.query(User).filter(User.email == args['email']).first()
        if not user:
            raise NotFound("Пользователь с таким email не найден")
        if not user.check_password(args['password']):
            return make_response(jsonify({'message': 'Неверный пароль'}), 401)
        return make_response(jsonify({'message': 'Успешный вход', 'user': {'id': user.id, 'email': user.email}}), 200)
