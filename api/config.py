
import os

base_dir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = "123abcd"

def config_app(app):
   app.config["SECRET_KEY"] = SECRET_KEY
   app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(base_dir, 'tasks.db')}"
   app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
   return app
