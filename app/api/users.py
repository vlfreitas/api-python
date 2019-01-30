from flask import jsonify, request
from app import db
from app.api import bp
from app.api.errors import bad_request
from app.models import User
from config import Config
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if user is not None:
        return jsonify(user.to_dict(include_email=True)), 200
    return bad_request("Usuário não existe.")


@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if 'username' not in data or 'email' not in data:
        return bad_request('É necessário nome de usuário e email')
    if User.query.filter_by(username=data['username']).first():
        return bad_request('Nome de usuário já esta em uso')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('Email já esta em uso')
    user = User()
    user.from_dict(data)
    user.requestQuantity = 50
    db.session.add(user)
    db.session.commit()
    logger.info("## Usuário %s cadastrado ##", user.username)
    return jsonify(user.to_dict(include_email=True)), 200


@bp.route('/users/<int:id>/filme', methods=['GET'])
def get_user_filmes(id):
    user = User.query.get(id)
    if user is not None:
        if request.args.get('s') is not None:
            if user.requestQuantity > 0:
                payload = request.args
                response = requests.get(Config.API_URL, params=payload)
                if response.status_code == 200:
                    user.requestQuantity -= 1
                    db.session.commit()
                    return jsonify(response.json())
                else:
                    return jsonify({"message": "Ocorreu um erro"}), response.status_code
            else:
                return bad_request("Usuário zerou sua quantidade de requisições")
        else:
            return bad_request("Necessário informar o titulo do filme")
        return jsonify(user.to_dict(include_email=True)), 200
    return bad_request("Usuário não existe.")


@bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    user = User.query.get(id)
    if User.query.filter_by(email=data['email']).first():
        logger.info("## Email escolhido pelo usuario %s já esta em uso ##", user.username)
        return bad_request("Email já esta em uso")
    user.email = data['email']
    db.session.commit()
    logger.info("## Email do usuário %s atualizado ##", user.username)
    return jsonify(user.to_dict(include_email=True)), 200


@bp.route('/users/<int:id>/delete', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if user is not None:
        db.session.delete(user)
        db.session.commit()
        logger.info("## Usuário %s deletado ##", user.username)
        return jsonify({'message':'Usuário deletado'}), 200
    logger.info("## Não existe usuários cadastrados para o id = %d ##", id)
    return bad_request("Usuário não existe")


