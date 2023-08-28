from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_oauthlib.client import OAuth
import mysql.connector
import requests

app = Flask(__name__)
app.config.from_pyfile('config.py')

app.secret_key = app.config['SECRET_KEY']  # Set a secret key for session

# Define your TMDB API key
TMDB_API_KEY = app.config['TMDB_API_KEY']

# Redirect URI for TMDB authentication
TMDB_REDIRECT_URI = 'http://localhost:5000/login/authorized'

# OAuth configuration for TMDB
oauth = OAuth(app)
tmdb = oauth.remote_app(
    'tmdb',
    consumer_key=TMDB_API_KEY,  # Use your TMDB API key here
    request_token_params={'scope': 'account:write_rating'},
    base_url='https://api.themoviedb.org/3/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://api.themoviedb.org/4/auth/request_token',
    authorize_url='https://www.themoviedb.org/auth/access',
)

# MySQL database configuration (replace with your credentials)
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Ishik@2741",
    "database": "movies",
}


# Function to fetch movie data from the database
def get_movies():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM movies")
    movies = cursor.fetchall()
    conn.close()
    return movies


# Function to update the rating of a movie
def rate_movie(movie_id, rating):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("UPDATE movies SET rating = %s WHERE id = %s", (rating, movie_id))
    conn.commit()
    conn.close()


# Function to authenticate a user (replace with your authentication logic)
def authenticate_user(username, password):
    if username == "your_username" and password == "your_password":
        return True
    return False

@app.route('/')
def index():
    # Fetch movie data from the database
    movies = get_movies()
    return render_template('index.html', movies=movies)

@app.route('/rate/<int:movie_id>', methods=['POST'])
def rate(movie_id):
    rating = float(request.form.get('rating', 0))

    if rating >= 1.0 and rating <= 10.0:
        # Use the user's access token to rate the movie on TMDB
        if 'tmdb_token' in session:
            tmdb_access_token = session['tmdb_token']
            result = rate_movie_on_tmdb(tmdb_access_token, movie_id, rating)
            if result:
                flash(f'You rated the movie with ID {movie_id} on TMDB!', 'success')
            else:
                flash('Failed to rate the movie on TMDB', 'error')
        else:
            flash('You need to log in with TMDB to rate movies', 'error')

    return redirect(url_for('index'))

@app.route('/login')
def login():
    # Redirect the user to TMDB for authentication
    auth_url = f'https://www.themoviedb.org/auth/access?request_token={TMDB_API_KEY}&redirect_to={TMDB_REDIRECT_URI}'
    return redirect(auth_url)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('index'))

@app.route('/login/authorized')
def authorized():
    # Handle TMDB authentication and token retrieval here
    request_token = request.args.get('request_token')
    
    # Exchange the request token for an access token using the TMDB API
    # You will need to make a POST request to TMDB's access token URL
    # Include the request token and your API key in the request
    # Parse the response to obtain the access token
    
    # Store the access token in the session
    session['tmdb_token'] = access_token

    # Flash a success message or an error message based on the authentication result
    # ...

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)