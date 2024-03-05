"""
This module contains a script for creating the database and tables for the application.

It includes the following:

- Importing necessary modules and the Flask application and SQLAlchemy instance.
- Checking if the database file already exists.
- If the database file does not exist, creating the tables in the database.
- Printing a message to indicate whether the database and tables were created or
 if the database already exists.

This script is run manually to set up the database for the application.
"""
import os
from to_do_list import app, db

# Check if database already exists
if not os.path.exists(r'to_do_list\data.sqlite'):
    # Create tables
    with app.app_context():
        db.create_all()
    print("Database and tables created")
else:
    print("Database already exists")
