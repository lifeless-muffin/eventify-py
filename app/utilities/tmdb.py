import os 
import requests
from algorithms.suggestion import suggest_content
from datetime import date, datetime, timedelta

# Retrieve api key
API_KEY = "3ac6f85f91f5f1947d9a8d7706fdf6b5"
BASE_URL = "https://api.themoviedb.org/3"


def fetch_content (type, region, categories):

    # request params
    params = {
        'sort_by': 'popularity.desc',
        'region': region,
        'with_genres': str(','.join(categories))
    }

    # calculate date range for movies
    gte_date = date.today() - timedelta(days=30)
    lte_date = date.today() + timedelta(days=15)

    # create lists for upcoming and now playing movies
    global upcoming_content
    global now_playing_content
    global combined_content

    upcoming_endpoint = f"{BASE_URL}/discover/{type}?api_key={API_KEY}&release_date.gte={date.today()}&release_date.lte={lte_date}&page=1"
    now_playing_endpoint = f"{BASE_URL}/discover/{type}?api_key={API_KEY}&release_date.gte={gte_date}&release_date.lte={date.today()}&page=1"

    print('upcoming url', upcoming_endpoint)
    print('now playing url', now_playing_endpoint)


    try: 

        response = requests.get(upcoming_endpoint, params=params)
        response.raise_for_status() # Raise an error if the response status code is not in the 2xx range
        upcoming_content = response.json()['results']

        response = requests.get(now_playing_endpoint, params=params)
        response.raise_for_status() # Raise an error if the response status code is not in the 2xx range
        now_playing_content = response.json()['results']

        combined_content = upcoming_content.copy()
        combined_content.extend(now_playing_content)   


    except requests.exceptions.RequestException as e:
        print(f"Something went wrong: {e}")
        return {'status': 'failed', 'message': 'Something went wrong'}, 500
    

    # remove duplicates based on movie ID
    ids = []
    unique_content = []

    for movie in combined_content:
        if movie['id'] not in ids:
            unique_content.append(movie)
            ids.append(movie['id'])

    return unique_content


def get_content(user):

    # retrieve user preferences 
    user_preferences = user['preferences']

    # fetch the content / both movies and tv shows
    fetched_movies = fetch_content('movie', 'us', ['27'])
    fetched_shows = fetch_content('tv', user_preferences['region'], ['27'])

    movies_and_shows_combined = fetched_movies.copy()
    movies_and_shows_combined.extend(fetched_shows)


    suggestions = suggest_content(num_suggestions=10, suggestion_frequency=1, content_list=movies_and_shows_combined)    
