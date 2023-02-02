from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_wtf.csrf import CSRFProtect
from flask_restful import Api, Resource, fields, marshal_with


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@localhost:3306/test_db'
app.config['SECRET_KEY'] = "random string"
app.app_context().push()
csrf = CSRFProtect(app)
csrf.init_app(app)

db = SQLAlchemy(app)
studend_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'city': fields.String,
    'addr': fields.String,
    'pin': fields.String,
    'created_at': fields.DateTime,
    'courses': fields.Integer
}


class Studends(Resource):
    @marshal_with(studend_fields)
    def get(self):
        students = Student.query.all()
        return students


api.add_resource(Studends, '/s_list')


student_course = db.Table('student_course', db.Model.metadata,
                          db.Column('student_id', db.Integer,
                                    db.ForeignKey('student.id')),
                          db.Column('course_id', db.Integer,
                                    db.ForeignKey('course.id'))
                          )


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(50))
    addr = db.Column(db.String(200))
    pin = db.Column(db.String(10))
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))

    def __init__(self, name, city, addr, pin):
        super().__init__()
        self.name = name
        self.city = city
        self.addr = addr
        self.pin = pin
        # self.courses=courses


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    student = db.relationship(
        'Student', backref=db.backref('course', lazy=True))

    def __init__(self, name) -> None:
        self.name = name


@app.route('/')
@csrf.exempt
def show_all():
    students = Student.query.all()
    return render_template('show_all.html', students=students)


@app.route('/details')
@csrf.exempt
def s_index():
    try:
        students = Student.query.all()
        return render_template('details.html', students=students)
    except Exception as e:
        pass


@app.route('/new', methods=['GET', 'POST'])
@csrf.exempt
def new():
    if request.method == 'POST':
        try:
            name = request.form['name']
            city = request.form['city']
            addr = request.form['addr']
            pin = request.form['pin']
            courses = []

            student = Student(name=name, city=city, addr=addr, pin=pin)
            for c in request.form.getlist('courses'):
                course = Course.query.get(c)
                courses.student = student
                courses.append(course)

            db.session.add(student)
            db.session.add_all(courses)
            db.session.commit()
            flash('Record was successfully added')
            return redirect(url_for('show_all'))
        except Exception as e:
            return e
    return render_template('new.html')


@app.route('/<int:student_id>/')
def stident_details(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('student_result.html', student=student)


@app.route('/add_course', methods=['POST', 'GET'])
def add_course():
    if request.method == 'GET':
        return render_template('course.html')
    else:
        course = Course(request.form['name'])

        db.session.add(course)
        db.session.commit()
        flash('Record was successfully added')
        return redirect(url_for('show_all'))


@app.route('/add_student')
def student():
    courses = Course.query.all()
    return render_template('student.html', courses=courses)


@app.route('/courses')
def courses():
    c = Course.query.all()
    return c


if __name__ == '__main__':
    #  db.drop_all()
    db.create_all()
    app.run(debug=True)
