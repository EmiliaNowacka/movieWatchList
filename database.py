import datetime
import sqlite3

CREATE_MOVIES_TABLE = """CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY,
    title TEXT, 
    release_timestamp REAL
);"""

CREATE_USERS_TABLE = """CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY
);"""

CREATE_WATCHED_TABLE = """CREATE TABLE IF NOT EXISTS watched (
    user_username TEXT, 
    movie_id INTEGER,
    FOREIGN KEY(user_username) REFERENCES users(username),
    FOREIGN KEY(movie_id) REFERENCES movies(id)
);"""

INSERT_MOVIES = "INSERT INTO movies (title, release_timestamp) VALUES (?, ?);"
INSERT_USER = "INSERT INTO users (username) VALUES (?);"
DELETE_MOVIE = "DELETE FROM movies WHERE title = ?;"
SELECT_ALL_MOVIES = "SELECT * FROM movies;"
SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_timestamp > ?;"
SELECT_WATCHED_MOVIES = """SELECT movies.* FROM movies 
JOIN watched ON movies.id = watched.movie_id 
JOIN users ON users.username = watched.user_username 
WHERE users.username = ?;"""
UPDATE_MOVIE_AS_WATCHED = "UPDATE movies SET watched = 1 WHERE title = ?;"
INSERT_WATCHED_MOVIE = "INSERT INTO watched (user_username, movie_id) VALUES (?,  ?);"
SET_MOVIE_WATCHED = "UPDATE movies SET watched = 1 WHERE title = ?;"
GET_MOVIE_ID = "SELECT id FROM movies WHERE EXISTS title = ?;"
CHECK_IF_USER_EXISTS = "SELECT username FROM users WHERE username = ?;"


connection = sqlite3.connect("data.db")


def create_tables():
    with connection:
        connection.execute(CREATE_MOVIES_TABLE)
        connection.execute(CREATE_USERS_TABLE)
        connection.execute(CREATE_WATCHED_TABLE)


def add_user(username):
    with connection:
        try:
            connection.execute(INSERT_USER, (username,))
        except sqlite3.IntegrityError:
            print("user already exists")


def add_movie(title, release_timestamp):
    with connection:
        connection.execute(INSERT_MOVIES, (title, release_timestamp))


def get_movies(upcoming=False):
    with connection:
        cursor = connection.cursor()
        if upcoming:
            today_timestamp = datetime.datetime.today().timestamp()
            cursor.execute(
                SELECT_UPCOMING_MOVIES, (today_timestamp,)
            )  # comma at the end cause it has to be a tuple!!
        else:
            cursor.execute(SELECT_ALL_MOVIES)
        return cursor.fetchall()


def get_movie_id_by_title(movie_title):
    with connection:
        return connection.execute(GET_MOVIE_ID, (movie_title,)).fetchone()


def check_user_exists(username):
    with connection:
        try:
            connection.execute(CHECK_IF_USER_EXISTS, (username,)).fetchone()
            print("user exists\n")
            return True
        except sqlite3.OperationalError:
            return False


def watch_movie(username, movie_title):
    user_exists = check_user_exists(username)
    if user_exists:
        try:
            movie_id = get_movie_id_by_title(movie_title)
        except sqlite3.OperationalError:
            print("Movie not yet in database, please add the movie first\n")
            return
        movie_id = movie_id[0]
        with connection:
            connection.execute(INSERT_WATCHED_MOVIE, (username, movie_id))
    else:
        print("User not exists in database please create user first")


def get_watched_movies(username):
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_WATCHED_MOVIES, (username,))
        return cursor.fetchall()
