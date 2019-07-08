from flask import Flask

clicker = Flask(__name__)

@clicker.route('/')

def home():
    return 'hello world'

if __name__ == '__main__':
    clicker.run()