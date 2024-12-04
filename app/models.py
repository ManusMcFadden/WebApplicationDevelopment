from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(db.Model, UserMixin):
    email = db.Column(db.String(500), primary_key=True)
    password = db.Column(db.String(500))
    weight = db.Column(db.Float)
    workouts = db.relationship('Workout', backref='user', lazy='dynamic')


    def set_password(self, inputPassword):
        self.password = generate_password_hash(inputPassword)

    def check_password(self, outputPassword):
        return check_password_hash(self.password, outputPassword)
    
    def get_id(self):
        return self.email
    
    def __repr__(self):
        return '{}{}{}'.format(self.email, self.password, self.weight)
    
class Exercise(db.Model):
    name = db.Column(db.String(500), primary_key=True)
    muscle = db.Column(db.String(500))
    equipment = db.Column(db.String(500))
    video = db.Column(db.String(500))
    workouts = db.relationship('Workout', backref='exercise', lazy='dynamic')

    def __repr__(self):
        return '{}{}{}{}'.format(self.name, self.muscle, self.equipment, self.video)

class Workout(db.Model):
    userEmail = db.Column(db.String(500), db.ForeignKey('user.email'), primary_key=True)
    exerciseName = db.Column(db.String(500), db.ForeignKey('exercise.name'), primary_key=True)
    date = db.Column(db.Date, primary_key=True)
    sets = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    weight = db.Column(db.Float)
    difficulty = db.Column(db.Integer)
    notes = db.Column(db.String(500))

    def __repr__(self):
        return '{}{}{}{}{}{}{}{}{}'.format(self.userEmail, self.exerciseName, self.date, self.sets, self.reps, self.weight, self.difficulty, self.notes)
