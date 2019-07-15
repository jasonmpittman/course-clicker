from flask import (
    Flask, render_template, request, flash, redirect, url_for, session
)
from models import db, Users
from werkzeug.security import generate_password_hash, check_password_hash

clicker = Flask(__name__)

#load config options
clicker.config.from_object('config')

db.init_app(clicker)
db.create_all(app=clicker)

# route for home
@clicker.route('/')
def home():
    return render_template('index.html')

@clicker.route('/polls')
def polls():
    if 'user' in session:
        user = Users.query.filter_by(username=session['user']).first()
        if user.role == 'faculty':
            return render_template('polls.html')
        else:
            return redirect(url_for('poll'))
    else:
        flash('Please login to access polls')
        return redirect(url_for('home'))

@clicker.route('/poll')
def poll():
    return render_template('poll.html')

@clicker.route('/attendance')
def attendance():
    if 'user' in session:
        user = Users.query.filter_by(username=session['user']).first()
        if user.role == 'faculty':
            return render_template('attendance.html')
        else:
            return redirect(url_for('attendee'))
    else:
        flash('Please login to access attendance')
        return redirect(url_for('home'))

# route for student attendee to submit attendance
@clicker.route('/attendee')
def attendee():
    return render_template('attendee.html')

# route for login handling
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
    
    return redirect(url_for('home'))

# route for logout handling
@clicker.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user')
        flash('Logout successful')
    
    return redirect(url_for('home'))

# route for signup handling
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

if __name__ == '__main__':
    clicker.run()