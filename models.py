from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# abstract base class for inheritance
class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

# question data model
class Questions(Base):
    question = db.Column(db.String(5000))

    def __repr__(self):
        return self.question

# answer data model
class Answers(Base):
    answer = db.Column(db.String(500))

# poll (question + answer choices) data model
class Polls(Base):
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    answer_id = db.Column(db.Integer, db.ForeignKey('answers.id'))
    vote_count = db.Column(db.Integer, default=0)
    status = db.Column(db.Boolean)

    #relations
    question = db.relationship('Questions', foreign_keys=[question_id],
        backref=db.backref('answers', lazy='dynamic'))
    
    answer = db.relationship('Answers', foreign_keys=[answer_id])

    def __repr__(self):
        return self.answer.name

class Users(Base):
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))