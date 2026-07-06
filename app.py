from flask import Flask, render_template, request, redirect

from models import db, Student
import os
app = Flask(__name__)





DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home():

    students = Student.query.all()

    return render_template("index.html", students=students)


@app.route("/add", methods=["GET","POST"])

def add():

    if request.method == "POST":

        student = Student(

            name=request.form["name"],

            email=request.form["email"],

            course=request.form["course"]

        )

        db.session.add(student)

        db.session.commit()

        return redirect("/")

    return render_template("add.html")


@app.route("/delete/<int:id>")

def delete(id):

    student = Student.query.get(id)

    db.session.delete(student)

    db.session.commit()

    return redirect("/")


@app.route("/edit/<int:id>", methods=["GET","POST"])

def edit(id):

    student = Student.query.get(id)

    if request.method == "POST":

        student.name = request.form["name"]

        student.email = request.form["email"]

        student.course = request.form["course"]

        db.session.commit()

        return redirect("/")

    return render_template("edit.html", student=student)


if __name__ == "__main__":
    app.run(debug=True, port=5020)