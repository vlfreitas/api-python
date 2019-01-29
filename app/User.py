from flask import request
from flask_restful import Resource
from app.models import db, User, UserSchema

users_schema = UserSchema(many=True)
user_schema = UserSchema()


class UserResource(Resource):
    def get(self):
        users = User.query.all()
        users = users_schema.dump(users).data
        return {'status': 'success', 'data': users}, 200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = user_schema.load(json_data)
        if errors:
            return errors, 422
        category = User.query.filter_by(name=data['name']).first()
        if category:
            return {'message': 'User already exists'}, 400
        category = User(
            name=json_data['name']
        )

        db.session.add(category)
        db.session.commit()

        result = user_schema.dump(category).data

        return {"status": 'success', 'data': result}, 201

    def put(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = user_schema.load(json_data)
        if errors:
            return errors, 422
        category = User.query.filter_by(id=data['id']).first()
        if not category:
            return {'message': 'Category does not exist'}, 400
        category.name = data['name']
        db.session.commit()

        result = user_schema.dump(category).data

        return {"status": 'success', 'data': result}, 204

    def delete(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = user_schema.load(json_data)
        if errors:
            return errors, 422
        category = User.query.filter_by(id=data['id']).delete()
        db.session.commit()

        result = user_schema.dump(category).data

        return {"status": 'success', 'data': result}, 204