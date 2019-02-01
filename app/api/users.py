from flask import jsonify, request
from app import db
from app.api import api
from app.models import User
from config import Config
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@api.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    """
    Method for return a user
    ---
    tags:
      - User
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: User ID
    responses:
      400:
        description: User does not exist
      200:
        description: Returns a user
    """
    user = User.query.get(id)
    if user is not None:
        return jsonify(id=user.id,
                       username=user.username,
                       email=user.email,
                       requestQuantity=user.requestQuantity), 200
    return jsonify(message="Usuário não existe."), 400


@api.route('/users', methods=['POST'])
def create_user():
    """
        Method for create a user
        ---
        tags:
          - User
        parameters:
          - name: body
            in: body
            required: true
            schema:
              properties:
                username:
                  type: string
                email:
                  type: string
        responses:
          400:
            description: Username and email not informed
          200:
            description: Can return user returned, email in use or username in use
    """
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


@api.route('/users/<int:id>/movie', methods=['GET'])
def get_user_movie(id):
    """
        Method to return all the movies registered in the OMDb API within the sent parameters
        ---
        tags:
          - User
        parameters:
          - name: id
            in: path
            type: integer
            required: true
            description: User ID
          - name: s
            in: query
            type: string
            required: true
            description: Movie title to search for
          - name: type
            in: query
            type: string
            description: Type of result to return (movie, series, episode)
          - name: y
            in: query
            type: string
            description: Year of release
        responses:
          404:
            description: User enter a non-existent ID
          400:
            description: User enter a non-existent ID or not report a title from the movie
          200:
            description: Returns a list of the movies / episodes / series found with the reported parameters and if a movie was not found
    """
    user = User.query.get(id)
    if user is not None:
        if request.args.get('s') is not None:
            if user.requestQuantity > 0:
                payload = request.args
                response = requests.get(Config.API_URL, params=payload)
                if 'Error' not in response.json():
                    user.requestQuantity -= 1
                    db.session.commit()
                    return jsonify(filmes=response.json()['Search']), 200
                else:
                    return jsonify(message=response.json()['Error']), 200
            else:
                return jsonify(message="Usuário zerou sua quantidade de requisições"), 200
        else:
            return jsonify(message="Necessário informar o titulo do filme"), 400
    return jsonify(message="Usuário não existe."), 404


@api.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    """
        Method for update a user
        ---
        tags:
          - User
        parameters:
          - name: id
            in: path
            type: integer
            required: true
            description: User ID
          - name: body
            in: body
            required: true
            schema:
              properties:
                email:
                  type: string
        responses:
          404:
            description: User enter a non-existent ID
          400:
            description: Email not informed
          200:
            description: Email chosen is in use or user email successfully updated
    """
    data = request.get_json()
    user = User.query.get(id)
    if user is not None:
        if 'email' not in data:
            return jsonify(message='É necessário informar um email'), 400
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
    return jsonify(message="Usuário não existe."), 404


@api.route('/users/<int:id>/delete', methods=['DELETE'])
def delete_user(id):
    """
        Method for delete a user
        ---
        tags:
          - User
        parameters:
          - name: id
            in: path
            type: integer
            required: true
            description: User ID
        responses:
          404:
            description: User enter a non-existent ID
          200:
            description: Deleted user
    """
    user = User.query.get(id)
    if user is not None:
        db.session.delete(user)
        db.session.commit()
        logger.info("## Usuário %s deletado ##", user.username)
        return jsonify({'message':'Usuário deletado'}), 200
    logger.info("## Não existe usuários cadastrados para o id = %d ##", id)
    return jsonify(message="Usuário não existe"), 404


