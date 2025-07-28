from app.extensions import db

class Subject(db.Model):
    __tablename__ = 'subject'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    level = db.Column(db.String(50), nullable= True)
    description = db.Column(db.Text, nullable=True)
    
    chapters = db.relationship('Chapter', back_populates='subject', cascade = 'all, delete-orphan')
    
    def __repr__(self):
        return f'<Subject {self.name}>'