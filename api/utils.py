from functools import wraps
from flask import jsonify, make_response, request
from config import SECRET_KEY
from entites import User, db
import jwt

def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
       token = None
       if 'x-access-tokens' in request.headers:
           token = request.headers['x-access-tokens']
       if not token:
           return make_response("a valid token is missing", 400, {'message': 'a valid token is missing'})
       data = jwt.decode(token, SECRET_KEY , algorithms=["HS256"])
       current_user = User.query.filter_by(id=data['id']).first()
       return f(current_user, *args, **kwargs)
   return decorator


def no_authorized():
    return make_response("no authorized", 401, {"authenticacion": "login required"})

def created(): 
    return make_response("created", 201)

def resource_not_found():
    return make_response("resource not found", 404)

def no_content(): 
    return make_response("no content", 204)

