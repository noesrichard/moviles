from flask import Flask, jsonify, make_response, request
from flask_cors import CORS

from utils import token_required, no_authorized
from config import config_app
from entites import Work, User, Task, db

from user_routes import users_blueprint
from task_routes import tasks_blueprint


app = Flask(__name__)
app = config_app(app)

db.init_app(app)
CORS(app)

app.register_blueprint(users_blueprint)
app.register_blueprint(tasks_blueprint)

# db.drop_all()
# db.create_all()


if __name__ == "__main__":
   app.run(debug=True)
