from flask import jsonify, make_response, request, Blueprint
from utils import token_required, no_authorized, created, resource_not_found, no_content
from entites import Work, User, Task, db
from config import SECRET_KEY


tasks_blueprint = Blueprint("tasks_blueprint", __name__)

@tasks_blueprint.route("/api/tasks", methods=['POST'])
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
   return created()

@tasks_blueprint.route("/api/tasks", methods=["GET"])
@token_required
def list_tasks(current_user):
   tasks = Task.query.join(Task.workers).filter_by(user_id=current_user.id).all()
   tasks += Task.query.filter_by(owner=current_user.id).join(Task.workers).all()
   if len(tasks) == 0:
      return no_content()

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
   return jsonify(response)

@tasks_blueprint.route("/api/tasks/<task_id>", methods=["GET"])
@token_required
def get_task_by_id(current_user, task_id):
   t = Task.query.filter_by(id=task_id).join(Task.workers).first()
   if t is None: 
      return resource_not_found()

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

@tasks_blueprint.route("/api/tasks/<task_id>", methods=["DELETE"])
@token_required
def delete_task(current_user, task_id):
   print(current_user.id)
   task = Task.query.filter_by(id=task_id).first()
   if task.owner == current_user.id:
      db.session.delete(task)
      db.session.commit()
      return make_response("deleted", 200)
   return no_authorized()

@tasks_blueprint.route("/api/tasks/<task_id>", methods=["PUT"])
@token_required
def update_task(current_user, task_id):
   data = request.get_json()
   task = Task.query.filter_by(id=task_id).first()

   if not task:
      return resource_not_found()

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
   return no_authorized()

@tasks_blueprint.route("/api/works/<task_id>", methods=["PUT"])
@token_required
def update_task_status(current_user, task_id):
   data = request.get_json()
   work = Work.query.filter_by(user_id=current_user.id, task_id=task_id).first()
   work.finished = data["finished"]
   db.session.commit()
   return make_response("modified", 200)

