from app.extensions import db
from datetime import datetime

class Quiz(db.Model):
    __tablename__ = 'quiz'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    date_of_quiz = db.Column(db.DateTime, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    time_duration = db.Column(db.Time, nullable=False)
    remarks = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.now, nullable=False)

    chapter = db.relationship('Chapter', back_populates='quizzes')
    questions = db.relationship('Question', back_populates='quiz', cascade='all, delete-orphan')
    scores = db.relationship('Score', back_populates='quiz', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Quiz {self.id} | Chapter {self.chapter_id}>'
