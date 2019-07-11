import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'course-clicker.db')
SECRET_KEY = 'secret_key'
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(DB_PATH)
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = True