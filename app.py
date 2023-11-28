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
            6 Add user
            7 Search for title
            8 EXIT
"""
welcome = "Welcome to the watchlist app"

print(welcome)
create_tables()


def prompt_add_movie():
    title = input("Movie title: \n")
    release_date = input("Release date (dd-mm-yyyy): \n")
    parsed_date = datetime.datetime.strptime(release_date, "%d-%m-%Y")
    timestamp = parsed_date.timestamp()
    add_movie(title, timestamp)


def prompt_add_user():
    _username = input("Username: ")
    add_user(_username)


def print_movie_list(_movies, heading="All"):
    print(f"---- {heading} movies ----")
    for _id, title, release_date in _movies:
        movie_date = datetime.datetime.fromtimestamp(release_date)
        readable_date = movie_date.strftime("%b %d %Y")
        print(f"{_id}: {title} (on {readable_date})")
    print("---------------\n")


def prompt_watch_movie():
    movie_id = input("Enter movie you've watched \n")
    _username = input("Your username: \n")
    watch_movie(_username, movie_id)


def prompt_search_movies():
    title = input("Search for:")
    _movies = search_movies(title)
    if _movies:
        for movie in _movies:
            print(movie[1])


while (user_input := input(menu)) != "8":
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
        username = input("Your username: \n")
        movies = get_watched_movies(username)
        if movies:
            print_movie_list(movies, f"{username}'s watched")
        else:
            print("No movies watched yet")
    elif user_input == "6":
        prompt_add_user()
    elif user_input == "7":
        prompt_search_movies()
    else:
        print("ERROR: Invalid input, try again")
