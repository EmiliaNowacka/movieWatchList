import datetime

import database
from database import *

menu = """ 
            Please select one of the following options:
            1 Add new movie
            2 View upcoming movies
            3 View all movies
            4 Watch a movie
            5 View watched movies
            6 EXIT
"""
welcome = "Welcome to the watchlist app"

print(welcome)
create_tables()


def prompt_add_movie():
    title = input("Movie title: \n")
    release_date = input("Release date (dd-mm-yyyy): \n")
    parsed_date = datetime.datetime.strptime(release_date, "%d-%m-%Y")
    timestamp = parsed_date.timestamp()

    database.add_movie(title, timestamp)


def print_movie_list(movies, heading="All"):
    print(f"---- {heading} movies ----")
    for movie in movies:
        movie_date = datetime.datetime.fromtimestamp(movie[1])
        readable_date = movie_date.strftime("%b %d %Y")
        print(f"{movie[0]} (on {readable_date})")
    print("---------------\n")


def prompt_watch_movie():
    movie_title = input("Enter movie you've watched \n")
    database.watch_movie(movie_title)


while (user_input := input(menu)) != "6":
    if user_input == "1":
        prompt_add_movie()
    elif user_input == "2":
        movies = get_movies(upcoming=True)
        print_movie_list(movies, "upcoming")
    elif user_input == "3":
        movies = get_movies()
        print_movie_list(movies)
    elif user_input == "4":
        prompt_watch_movie()
    elif user_input == "5":
        pass
    else:
        print("ERROR: Invalid input, try again")
