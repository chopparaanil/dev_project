from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))

    email = db.Column(db.String(100))

    course = db.Column(db.String(100))

    def __repr__(self):
        return self.name