# config.py
import os

# Flask app configuration
DEBUG = True  # Set to False in production
SECRET_KEY = os.urandom(32)  # Replace with a strong secret key

# # Database configuration
# SQLALCHEMY_DATABASE_URI = 'mysql://username:password@localhost/database_name'
# SQLALCHEMY_TRACK_MODIFICATIONS = False  # Set to False to disable SQLAlchemy modification tracking

# TMDB API key
TMDB_API_KEY = 'aa10c9cf08a51fcb22613d4b62c94ca6'
