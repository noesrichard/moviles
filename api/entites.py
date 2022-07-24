from flask_sqlalchemy import Model, SQLAlchemy 
from sqlalchemy import Column, ForeignKey, Boolean, Integer, String
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Work(db.Model):
   task_id = db.Column(db.ForeignKey("task.id"), primary_key=True)
   user_id = db.Column(db.ForeignKey("user.id"), primary_key=True)
   finished = db.Column(db.Boolean, default=False)
   user = relationship("User")

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
   workers = relationship("Work", cascade="all,delete")


