import json
import os


WATCHLIST_FILE = 'watchlist.json'


def load_watchlist():
    if not os.path.exists(WATCHLIST_FILE):
        return []
    with open(WATCHLIST_FILE, 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

def save_watchlist(watchlist):
    with open(WATCHLIST_FILE, 'w') as file:
        json.dump(watchlist, file)

def add_movie(movie_id, movie_details):
    watchlist = load_watchlist()
    movie = {'movie_id': movie_id, 'movie_details': movie_details}
    watchlist.append(movie)
    save_watchlist(watchlist)
    return f'Movie with id {movie_id} added.'

def delete_movie(movie_id):
    watchlist = load_watchlist()
    updated_watchlist = [movie for movie in watchlist if movie['movie_id'] != movie_id]
    if len(updated_watchlist) == len(watchlist):
        return f'Movie with ID {movie_id} not found.'
    save_watchlist(updated_watchlist)
    return f'Movie with ID {movie_id} deleted.'

def list_movies():
    watchlist = load_watchlist()
    return watchlist


API_ENDPOINTS = {
    'add_movie': {
        'function': add_movie,
        'required_params': ['movie_id', 'movie_details']
    },
    'delete_movie': {
        'function': delete_movie,
        'required_params': ['movie_id']
    },
    'list_movies': {
        'function': list_movies,
        'required_params': []
    }
}

__all__ = [API_ENDPOINTS]