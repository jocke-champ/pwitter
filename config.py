import os

# Grab the folder where this script lives
basedir = os.path.abspath(os.path.dirname(__file__))

# Update the database URI to point to our local SQLite database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')