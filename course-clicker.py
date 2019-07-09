from flask import Flask
from models import db

clicker = Flask(__name__)

#load config options
clicker.config.from_object('config')

db.init_app(clicker)
db.create_all(app=clicker)

@clicker.route('/')

def home():
    return 'hello world'

if __name__ == '__main__':
    clicker.run()