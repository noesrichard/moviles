from flask import Flask, jsonify, make_response, request
from werkzeug.security import generate_password_hash,check_password_hash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from flask_cors import CORS
import datetime
import jwt
import os

base_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
CORS(app)

app.config["SECRET_KEY"] = "123abcd"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(base_dir, 'tasks.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class Work(db.Model):
   task_id = db.Column(db.ForeignKey("task.id"), primary_key=True)
   user_id = db.Column(db.ForeignKey("user.id"), primary_key=True)
   finished = db.Column(db.Boolean, default=False)
   user = db.relationship("User")

class User(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String(50))
   password = db.Column(db.String(50))

class Task(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   owner = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
   title = db.Column(db.String(50))
   subtitle = db.Column(db.String(50))
   deadline = db.Column(db.String(50))
   category = db.Column(db.String(30))
   priority = db.Column(db.String(20))
   workers = db.relationship("Work", cascade="all,delete")

# db.drop_all()
# db.create_all()

def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
       token = None
       if 'x-access-tokens' in request.headers:
           token = request.headers['x-access-tokens']
       if not token:
           return jsonify({'message': 'a valid token is missing'})
       try:
           data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
           current_user = User.query.filter_by(id=data['id']).first()
       except:
           return jsonify({'message': 'token is invalid'})
       return f(current_user, *args, **kwargs)
   return decorator

@app.route('/api/signup', methods=['POST'])
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

@app.route('/api/login', methods=['GET'])
def login():
   auth = request.authorization
   print(request.headers)
   if not auth:
       return make_response('could not verify, no authorization in request', 401, {'Authentication': 'login required"'})

   if not auth.username or not auth.password: 
       return make_response('could not verify, no username or password', 401, {'Authentication': 'login required"'})

   user = User.query.filter_by(username=auth.username).first()

   if user.password == auth.password:
       token = jwt.encode({'id' : user.id,
                           'exp' : datetime.datetime.utcnow() + datetime.timedelta(hours=24)},
                          app.config['SECRET_KEY'], "HS256")
       return jsonify({'token' : token, 'userId': user.id, "username": user.username})
   return make_response('could not verify',  401, {'Authentication': '"login required"'})

@app.route("/api/tasks", methods=['POST'])
@token_required
def create_task(current_user):
   data = request.get_json()
   owner = current_user.id
   workers = [User.query.filter_by(id=d["worker_id"]).first() for d in data["workers"]]
   new_task = Task(owner=owner,
                  title=data["title"],
                  subtitle=data["subtitle"],
                  deadline=data["deadline"],
                  category=data["category"],
                  priority=data["priority"])

   works = [Work(task_id=new_task.id, user_id=worker.id) for worker in workers]
   for work in works: 
      new_task.workers.append(work)

   db.session.add(new_task)
   db.session.commit()
   return make_response("created", 201)

@app.route("/api/tasks", methods=["GET"])
@token_required
def list_tasks(current_user):
   tasks = Task.query.join(Task.workers).filter_by(user_id=current_user.id).all()
   tasks += Task.query.filter_by(owner=current_user.id).join(Task.workers).all()
   tasks = list(dict.fromkeys(tasks))
   response = [{"id": t.id,
                "title": t.title,
                "subtitle": t.subtitle,
                "deadline": t.deadline,
                "category": t.category,
                "priority": t.priority,
                "workers": [{
                   "worker_id": w.user.id,
                   "username": w.user.username,
                   "finished": w.finished
                } for w in t.workers]} for t in tasks]
   print(response)
   return jsonify(response)

@app.route("/api/tasks/<task_id>", methods=["GET"])
@token_required
def get_task_by_id(current_user, task_id):
   t = Task.query.filter_by(id=task_id).join(Task.workers).first()
   if t is None: 
      return make_response("no resource", 404)
   response = {"id": t.id,
                "title": t.title,
                "subtitle": t.subtitle,
                "deadline": t.deadline,
                "category": t.category,
                "priority": t.priority,
                "workers": [{
                   "worker_id": w.user.id,
                   "username": w.user.username,
                   "finished": w.finished
                } for w in t.workers]} 
   return jsonify(response)

@app.route("/api/tasks/<task_id>", methods=["DELETE"])
@token_required
def delete_task(current_user, task_id):
   print(current_user.id)
   task = Task.query.filter_by(id=task_id).first()
   if task.owner == current_user.id:
      db.session.delete(task)
      db.session.commit()
      return make_response("deleted", 200)
   return make_response("you dont have permissions", 403)

@app.route("/api/tasks/<task_id>", methods=["PUT"])
@token_required
def update_task(current_user, task_id):
   data = request.get_json()
   task = Task.query.filter_by(id=task_id).first()
   if task.owner == current_user.id:
      task.title=data["title"]
      task.subtitle=data["subtitle"]
      task.deadline=data["deadline"]
      task.category=data["category"]
      task.priority=data["priority"]
      workers = [User.query.filter_by(id=d["worker_id"]).first() for d in data["workers"]]
      works = [Work(task_id=task.id, user_id=worker.id) for worker in workers]
      #task.workers = workers
      db.session.commit()
      return make_response("updated", 200)
   return make_response("you dont have permissions", 403)

@app.route("/api/works/<task_id>", methods=["PUT"])
@token_required
def update_task_status(current_user, task_id):
   data = request.get_json()
   work = Work.query.filter_by(user_id=current_user.id, task_id=task_id).first()
   work.finished = data["finished"]
   db.session.commit()
   return make_response("modified", 200)

if __name__ == "__main__":
   app.run(debug=True)
