from flask import (
    Flask, render_template, request, flash, redirect, url_for, session
)
from models import db
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
    
        password = generate_password_hash(password)

        user = Users(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        flash('Signup complete. Please login to continue.')

        return redirect(url_for('home'))
    
    return render_template('signup.html')

if __name__ == '__main__':
    clicker.run()