# Import necessary modules from the app package
from app import app, db
from app.models import User
from werkzeug.security import generate_password_hash

# Create the database and add an admin user if none exist
with app.app_context():
    db.create_all()
    # Check if there are any users in the database
    if User.query.count() == 0:
        print("Creating initial admin user")
        # Add an admin user with a hashed password
        user = User(
            username='admin',
            password=generate_password_hash('admin', method='pbkdf2:sha256', salt_length=16),
            security_question='Default question',
            security_answer='Default answer',
            is_admin=True
        )
        db.session.add(user)
        db.session.commit()
        print("Admin user created")
    else:
        print("Admin user already exists")
