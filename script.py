import requests
import json
import mysql.connector

# Get your TMDB API key from https://www.themoviedb.org/settings/api
API_KEY = "aa10c9cf08a51fcb22613d4b62c94ca6"

# Connect to the MySQL database
conn = mysql.connector.connect(host="localhost", user="root", password="Ishik@2741", database="movies")

# Create a cursor
cursor = conn.cursor()

# Get the JSON data from the TMDB API
url = f"https://api.themoviedb.org/3/movie/top_rated?api_key={API_KEY}"
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    
    # Iterate over the movies and insert them into the database
    for movie in data.get("results", []):
        title = movie.get("title", None)
        release_date = movie.get("release_date", None)
        year = release_date.split("-")[0] if release_date else None
        genres = ", ".join([genre["name"] for genre in movie.get("genres", [])])
        rating = movie.get("vote_average", None)

        # Use parameterized queries to insert data safely
        insert_query = "INSERT INTO movies (title, year, genre, rating) VALUES (%s, %s, %s, %s)"
        values = (title, year, genres, rating)

        cursor.execute(insert_query, values)

    # Commit the changes to the database
    conn.commit()
else:
    print("Error: Unable to fetch data from TMDB API")

# Close the connection to the database
conn.close()