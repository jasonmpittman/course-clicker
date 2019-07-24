#!/usr/bin/env python3

from flask import (
    Flask, render_template, request, flash, redirect, url_for, session
)
from flask_admin import Admin
from admin import AdminView
from models import db, Users, Polls, Questions, Answers, Attendance
from werkzeug.security import generate_password_hash, check_password_hash

clicker = Flask(__name__)

# load config options
clicker.config.from_object('config')

db.init_app(clicker)
db.create_all(app=clicker)

# instantiate flask admin
admin = Admin(clicker, name='Dashboard', index_view=AdminView(Users, db.session, url='/admin', endpoint='admin'))

# build admin views
admin.add_view(AdminView(Users, db.session))
#admin.add_view(AdminView(Polls, db.session))
#admin.add_view(AdminView(Questions, db.session))
#admin.add_view(AdminView(Answers, db.session))
admin.add_view(AdminView(Attendance, db.session))

# route for home
@clicker.route('/')
def home():
    return render_template('index.html')

#region route for REST API to polls
@clicker.route('/api/polls', methods=['GET', 'POST'])
def api_polls():
    if request.method == 'POST':
        poll = request.get_json()
    
        for key, value in poll.items():
            if not value:
                return jsonify({'error': 'value for {} is empty'.format(key)})

        question = poll['question']
        answers_query = lambda answer : Answers.query.filter(Answers.name.like(answer))

        answers = [Polls(answer=Answers(name=answer)) for answer in poll['answers']]

        new_question = Questions(question=question, answers=answers)

        db.session.add(new_question)
        db.session.commit()

        return jsonify({'message': 'Poll was created successfully'}) 
    
    else:
        polls = Questions.query.join(Polls).all()
        all_polls = {'Polls': [poll.to_json() for poll in polls]}
    
    return jsonify(all_polls)
#endregion

#region route for REST API for answers
@clicker.route('/api/polls/answers')
def api_polls_answers():
    all_answers = [answer.to_json() for answer in Answers.query.all()]

    return jsonify(all_answers)

@clicker.route('/polls', methods=['GET'])
def polls():
    if 'user' in session:
        return render_template('polls.html')
    else:
        flash('Please login to access polls')
        return redirect(url_for('home'))
#endregion

@clicker.route('/api/attendance', methods=['POST', 'GET'])
def api_attendance():
    if request.method == 'POST':
        attendance = request.get_json()

        return "Attendance for {} in course {} with keyword {}".format(attendance['user'], ['course'], ['keyword'])
    else:
        all_attendance = {}

        attendance = Attendance.query.all()
        for attendee in attendance:
            all_attendance[attendee.user] = {'user': [Attendance.user_id for user in User.query.filter_by(user_id=user_id)]}
        
        return jsonify(all_attendance)

@clicker.route('/attendance')
def attendance():
    if 'user' in session:
        return render_template('attendance.html')
    else:
        flash('Please login to access attendance')
        return redirect(url_for('home'))

#region route for login handling
@clicker.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = Users.query.filter_by(username=username).first()

    if user:
        password_hash = user.password

        if check_password_hash(password_hash, password):
            session['user'] = username
            flash('Login successful')
    else:
        flash('Username or password is incorrect')
    
    return redirect(request.args.get('next') or url_for('home'))
#endregion

#region route for signup handling
@clicker.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = 'student'

        password = generate_password_hash(password)

        user = Users(username=username, password=password, role=role)
        
        db.session.add(user)
        db.session.commit()

        flash('Signup complete. Please login to continue.')

        return redirect(url_for('home'))
    
    return render_template('signup.html')
#endregion

#region route for logout handling
@clicker.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user')
        flash('Logout successful')
    
    return redirect(url_for('home'))
#endregion

if __name__ == '__main__':
    clicker.run()