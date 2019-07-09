from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# abstract base class for inheritance
class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

class Questions(Base):
    question = db.Column(db.String(5000))

    def __repr__(self):
        return self.question

class Answers(Base):
    answer = db.Column(db.String(500))

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