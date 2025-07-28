from dotenv import load_dotenv
import os
from datetime import datetime
from app.extensions import db
from app.models import User, RoleEnum

load_dotenv()

def initialize_admin():
    admin_username = os.getenv('ADMIN_USERNAME', 'admin@example.com')
    admin_password = os.getenv('ADMIN_PASSWORD', 'admin123') 
    existing_admin = User.query.filter_by(role=RoleEnum.ADMIN).first()

    if not existing_admin:
        admin = User(
            username=admin_username,
            full_name='Quiz Master',
            qualification='Administrator',
            dob=datetime.strptime('1970-01-01', '%Y-%m-%d').date(),
            role=RoleEnum.ADMIN,
            status='active',
            is_verified=True,
            created_at=datetime.now(),
            notifications_enabled=False
            )
        admin.set_password(admin_password)  

        db.session.add(admin)
        db.session.commit()
        print("Admin initialized.")
    else:
        print("Admin already exists.")
