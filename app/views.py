from flask import render_template, flash, redirect, jsonify, request
from app import app, db, models
from .forms import SignupForm, LoginForm, WorkoutForm
from .models import User, Exercise, Workout
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime
import logging

def get_exercises():
    app.logger.info('get_exercises request')
    return {e.name: {'muscle': e.muscle, 'equipment': e.equipment, 'video': e.video} for e in Exercise.query.all()}

@app.route('/suggest_exercises', methods=['GET'])
def suggest_exercises():
    app.logger.info('suggest_exercies request')
    query = request.args.get('q', '').lower()
    suggestions = [exercise.name for exercise in Exercise.query.filter(Exercise.name.ilike(f"%{query}%")).all()]
    return jsonify({'suggestions': suggestions})


@app.route('/get_exercise/<exercise_name>', methods=['GET'])
def get_exercise(exercise_name):
    app.logger.info(f'get_exercise request for {exercise_name}')
    exercise = Exercise.query.filter_by(name=exercise_name).first()
    if exercise:
        app.logger.info(f'Exercise found: {exercise_name}')
        return jsonify({
            'muscle': exercise.muscle,
            'equipment': exercise.equipment,
            'video_url': exercise.video
        })
    return jsonify({'error': 'Exercise not found'}), 404

@app.route('/first', methods=['GET', 'POST'])
@login_required
def first():
    app.logger.info('first route request')
    if not current_user.is_authenticated:
        app.logger.info('User not authenticated')
        flash("You must be logged in to view this page.")
        return redirect('/login')
    form = WorkoutForm()
    exercises = Exercise.query.all()
    form.workout.choices = [(e.name, e.name) for e in exercises]

    if form.validate_on_submit():
        app.logger.info('Workout form submitted')
        exercise_name = form.workout.data
        w = models.Workout(
            userEmail=current_user.get_id(),
            date=datetime.utcnow(),
            exerciseName=exercise_name,
            sets=form.sets.data,
            reps=form.reps.data,
            weight=form.weight.data,
            difficulty=form.difficulty.data,
            notes=form.notes.data
        )
        db.session.add(w)
        db.session.commit()
        flash('Workout logged successfully')
        return redirect('/first')
    return render_template("first.html", title="Log workout", form=form)

@app.route('/', methods=['GET', 'POST'])
def home():
    app.logger.info('index route request')
    home={'description':'Welcome to the NextRep application, your personal workout assistant. Please sign up or log in to continue.'}
    return render_template('home.html', title='Home', home=home)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    app.logger.info('signup route request')
    form = SignupForm()
    if form.validate_on_submit():
        app.logger.info('Signup form submitted')
        if User.query.filter_by(email=form.email.data).first():
            app.logger.info('Email already in use')
            flash('Somebody has already signed up to NextRep with this email')
            return redirect('/signup')
        s = models.User(email=form.email.data)
        s.set_password(form.password1.data)
        db.session.add(s)
        db.session.commit()
        flash('Successfully signed up to NextRep')
        return redirect('/login')
    return render_template('signup.html',
                           title='Signup',
                           form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    app.logger.info('login route request')
    form = LoginForm()
    if form.validate_on_submit():
        app.logger.info('Login form submitted')
        u = User.query.filter_by(email=form.email.data).first()
        if u is None:
            app.logger.info('Invalid email')
            flash('Invalid email')
            return redirect('/login')
        if not u.check_password(form.password.data):
            app.logger.info('Invalid password')
            flash('Invalid password')
            return redirect('/login')
        login_user(u)
        flash('Logged in successfully')
        return redirect('/first')
    return render_template('login.html',
                           title='Login',
                           form=form)

@app.route('/logout')
def logout():
    app.logger.info('logout route request')
    logout_user()
    flash('Logged out successfully')
    return redirect('/')

@app.route('/userdetails', methods=['GET', 'POST'])
@login_required
def userdetails():
    app.logger.info('userdetails route request')
    user = User.query.filter_by(email=current_user.email).first()
    workouts = Workout.query.filter_by(userEmail=current_user.email).count()

    if request.method == 'POST':
        app.logger.info('User details form submitted')
        new_weight = request.form.get('weight')
        try:
            user.weight = float(new_weight)
            db.session.commit()
            flash("Weight updated successfully!", "success")
        except ValueError:
            flash("Invalid weight value!", "danger")
        return redirect('/userdetails')

    return render_template('userdetails.html', user=user, workouts=workouts, title='User Details')

@app.route('/workouts', methods=['GET'])
@login_required
def workouts():
    app.logger.info('workouts route request')
    user_workouts = Workout.query.filter_by(userEmail=current_user.email).all()
    return render_template('workouts.html', title='Workouts', workouts=user_workouts)

@app.route('/rpecalc', methods=['GET'])
@login_required
def rpecalc():
    app.logger.info('rpecalc route request')
    workouts = Workout.query.filter_by(userEmail=current_user.email).all()
    exercise_data = {}
    for workout in workouts:
        if workout.exerciseName not in exercise_data:
            app.logger.info(f'Adding exercise {workout.exerciseName} to data')
            exercise_data[workout.exerciseName] = []
        exercise_data[workout.exerciseName].append({
            'weight': workout.weight,
            'reps': workout.reps,
            'rpe': workout.difficulty
        })
    return render_template('rpecalc.html', title='RPE Calculator', exercises=exercise_data)
