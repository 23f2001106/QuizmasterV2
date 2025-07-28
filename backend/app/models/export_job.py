import enum
from app.extensions import db
from datetime import datetime

class ExportStatus(enum.Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"

class ExportJob(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filename = db.Column(db.String, nullable=True)
    status = db.Column(db.Enum(ExportStatus), default=ExportStatus.pending)
    created_at = db.Column(db.DateTime, default=datetime.now)
    completed_at = db.Column(db.DateTime, nullable=True)

    user = db.relationship('User', backref='export_jobs')
