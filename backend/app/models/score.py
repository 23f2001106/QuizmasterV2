from app.extensions import db
from datetime import datetime

class Score(db.Model):
    __tablename__ = 'score'

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    time_stamp_of_attempt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    total_scored = db.Column(db.Integer, nullable=False)
    time_taken = db.Column(db.Float, nullable=False)

    user = db.relationship('User', back_populates='scores')
    quiz = db.relationship('Quiz', back_populates='scores')

    def __repr__(self):
        return f'<Score {self.total_scored}, Time Taken: {self.time_taken}>'