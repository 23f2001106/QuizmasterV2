from app.extensions import db
from datetime import datetime, time
from werkzeug.security import generate_password_hash, check_password_hash
from enum import Enum

class RoleEnum(str, Enum):
    ADMIN = "admin"
    USER = "user"

class UserStatusEnum(str, Enum):
    INACTIVE = "inactive"
    ACTIVE = "active"
    SUSPENDED = "suspended"

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    
    username = db.Column(db.String(80), unique=True, nullable=False)  # can be email
    password_hash = db.Column(db.String(128), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    qualification = db.Column(db.String(100), nullable=True)
    dob = db.Column(db.Date, nullable=True)
    
    role = db.Column(db.Enum(RoleEnum), default=RoleEnum.USER, nullable=False)
    status = db.Column(db.Enum(UserStatusEnum), default=UserStatusEnum.INACTIVE, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.now)
    last_login = db.Column(db.DateTime, nullable=True)

    notifications_enabled = db.Column(db.Boolean, default=True)
    preferred_reminder_time = db.Column(db.Time, default=time(hour=18, minute=0))  # Default 6 PM
    is_verified = db.Column(db.Boolean, default=False)  # Email or account verification

    scores = db.relationship('Score', back_populates='user', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Role Checker
    def is_admin(self):
        return self.role == RoleEnum.ADMIN

    def is_active(self):
        return self.status == UserStatusEnum.ACTIVE

    def __repr__(self):
        return f"<User {self.username} - {self.role}>"


class ReminderLog(db.Model):
    __tablename__ = 'reminder_log'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reminder_date = db.Column(db.Date, nullable=False)  # Date when reminder was sent
    sent_at = db.Column(db.DateTime, default=datetime.now)

    user = db.relationship('User', backref='reminder_logs')
