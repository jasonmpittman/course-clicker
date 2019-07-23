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
    
    def to_json(self):
        return {
            'question': self.question,
            #'options': [Polls(answer=Answers(name=answer))
                #if answers_query(answer).count() == 0
                #else Polls(answer=answers_query(answer).first()) for answer in poll['answers']
            #],
            'options': 
                [{'name': option.option.name, 'vote_count': option.vote_count}
                    for option in self.options.all()],
            'status': self.status
        }

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

# user data model
class Users(Base):
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))
    role = db.Column(db.String(7))

# attendance data model
class Attendance(Base):
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    keyword = db.Column(db.String(100))
    course = db.Column(db.String(7))

    def to_json(self):
        return {
            'user': self.user_id,
            'course': self.course,
            'keyword': self.keyword  

        }