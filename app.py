import configparser
import os
from flask import Flask, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy_requests
import cache_token


# Authenticate spotify account
def authenticate_sp():
    config = configparser.ConfigParser()
    config_file_path = os.path.join(os.path.dirname(__file__), 'config.cfg')

    # Spotify API credentials
    config.read(config_file_path)
    client_id = config.get('api_keys', 'client_id')
    client_secret = config.get('api_keys', 'client_secret')
    redirect_uri = config.get('api_keys', 'redirect_uri')

    return cache_token.authenticate_spotify()


sp = authenticate_sp()
app = Flask(__name__)


# Web scraping function (example: scrape quotes from a site)
def scrape_data(type_of_req, term):
    return spotipy_requests.getCurrentUserTopItems(sp, type_of_req, term)


@app.route('/')
def home():
    list1 = scrape_data('artists', 'short')
    list2 = scrape_data('artists', 'medium')
    list3 = scrape_data('artists', 'long')
    list4 = scrape_data('tracks', 'short')
    list5 = scrape_data('tracks', 'medium')
    list6 = scrape_data('tracks', 'long')

    return render_template('index.html', list1=list1,
                           list2=list2,
                           list3=list3,
                           list4=list4,
                           list5=list5,
                           list6=list6)


if __name__ == '__main__':
    app.run(debug=True)
