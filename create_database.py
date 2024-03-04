import os
from to_do_list import app, db

# Check if database already exists
if not os.path.exists('to_do_list\data.sqlite'):
    # Create tables
    with app.app_context():
        db.create_all()
    print("Database and tables created")
else:
    print("Database already exists")