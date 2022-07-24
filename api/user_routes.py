from flask import Flask, jsonify, make_response, request, Blueprint
from entites import User, db
from utils import no_authorized
from config import SECRET_KEY
import jwt
import datetime

users_blueprint = Blueprint("users_blueprint", __name__)

@users_blueprint.route('/api/signup', methods=['POST'])
def signup():
   data = request.get_json()

   username = data["username"]
   password = data["password"]

   user = User.query.filter_by(username=username).first()

   if user is not None:
      return make_response('username alredy picked', 500)

   new_user = User(username=username, password=password)

   db.session.add(new_user)
   db.session.commit()

   return jsonify({'message': 'registered successfully'})

@users_blueprint.route('/api/login', methods=['GET'])
def login():
   auth = request.authorization
   if not auth or not auth.username or not auth.password:
      return no_authorized()

   user = User.query.filter_by(username=auth.username).first()

   if user.password == auth.password:
      exp = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
      token = jwt.encode({'id' : user.id, 'exp' : exp}, SECRET_KEY, "HS256")

      return jsonify({"token" : token,
                      "userId": user.id,
                      "username": user.username})

   return no_authorized()



