from dotenv import load_dotenv
import os


load_dotenv()

MOVIE_WATCHLIST_PORT = os.getenv('MOVIE_WATCHLIST_PORT')
