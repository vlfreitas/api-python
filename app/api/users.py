from flask import jsonify, request
from app import db
from app.api import api
from app.api.errors import bad_request
from app.models import User
from config import Config
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@api.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if user is not None:
        return jsonify(id=user.id,
                       username=user.username,
                       email=user.email,
                       requestQuantity=user.requestQuantity), 200
    return jsonify(message="Usuário não existe."), 400


@api.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if 'username' not in data or 'email' not in data:
        return jsonify(message='É necessário nome de usuário e email'), 400
    if User.query.filter_by(username=data['username']).first():
        return jsonify(message='Nome de usuário já esta em uso'), 200
    if User.query.filter_by(email=data['email']).first():
        return jsonify(message='Email já esta em uso'), 200
    user = User(data['username'], data['email'])
    user.requestQuantity = 50
    db.session.add(user)
    db.session.commit()
    logger.info("## Usuário %s cadastrado ##", user.username)
    return jsonify(id=user.id,
                   username=user.username,
                   email=user.email,
                   requestQuantity=user.requestQuantity), 201


@api.route('/users/<int:id>/filme', methods=['GET'])
def get_user_filmes(id):
    user = User.query.get(id)
    if user is not None:
        if request.args.get('s') is not None:
            if user.requestQuantity > 0:
                payload = request.args
                response = requests.get(Config.API_URL, params=payload)
                if response.json()['Error'] is None:
                    user.requestQuantity -= 1
                    db.session.commit()
                    return jsonify(filmes=response.json()['Search']), 200
                else:
                    return jsonify(message=response.json()['Error']), 200
            else:
                return jsonify(message="Usuário zerou sua quantidade de requisições"), 200
        else:
            return jsonify(message="Necessário informar o titulo do filme"), 400
    return jsonify(message="Usuário não existe."), 400


@api.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    user = User.query.get(id)
    if User.query.filter_by(email=data['email']).first():
        logger.info("## Email escolhido pelo usuario %s já esta em uso ##", user.username)
        return jsonify(message="Email já esta em uso"), 200
    user.email = data['email']
    db.session.commit()
    logger.info("## Email do usuário %s atualizado ##", user.username)
    return jsonify(id=user.id,
                   username=user.username,
                   email=user.email,
                   requestQuantity=user.requestQuantity), 200


@api.route('/users/<int:id>/delete', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if user is not None:
        db.session.delete(user)
        db.session.commit()
        logger.info("## Usuário %s deletado ##", user.username)
        return jsonify({'message':'Usuário deletado'}), 200
    logger.info("## Não existe usuários cadastrados para o id = %d ##", id)
    return jsonify(message="Usuário não existe"), 400


