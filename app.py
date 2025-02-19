import configparser
import os
import queue
import threading

from flask import Flask, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy_requests


def authenticate_sp():
    config = configparser.ConfigParser()
    config_file_path = os.path.join(os.path.dirname(__file__), 'config.cfg')

    config.read(config_file_path)
    client_id = config.get('api_keys', 'client_id')
    client_secret = config.get('api_keys', 'client_secret')
    redirect_uri = config.get('api_keys', 'redirect_uri')

    TOKEN_CACHE_PATH = 'token_cache.json'
    # sp = cache_token.authenticate_spotify()
    return spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                     client_secret=client_secret,
                                                     redirect_uri=redirect_uri,
                                                     scope="user-library-read,user-top-read"))


sp = authenticate_sp()
app = Flask(__name__)


# Web scraping function (example: scrape quotes from a site)
def scrape_data(q, type_of_req, term):
    topItems = spotipy_requests.getCurrentUserTopItems(sp, type_of_req, term)

    q.put(topItems)


@app.route('/')
def home():
    threads = []
    q = queue.Queue()
    thread1 = threading.Thread(target=scrape_data, args=(q, 'artists', 'short'))
    thread2 = threading.Thread(target=scrape_data, args=(q, 'artists', 'medium'))
    thread3 = threading.Thread(target=scrape_data, args=(q, 'artists', 'long'))
    thread4 = threading.Thread(target=scrape_data, args=(q, 'tracks', 'short'))
    thread5 = threading.Thread(target=scrape_data, args=(q, 'tracks', 'medium'))
    thread6 = threading.Thread(target=scrape_data, args=(q, 'tracks', 'long'))
    thread6.start()
    thread5.start()
    thread4.start()
    thread3.start()
    thread2.start()
    thread1.start()
    threads.append(thread6)
    threads.append(thread5)
    threads.append(thread4)
    threads.append(thread3)
    threads.append(thread2)
    threads.append(thread1)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    list1 = q.get()
    list2 = q.get()
    list3 = q.get()
    list4 = q.get()
    list5 = q.get()
    list6 = q.get()

    return render_template('index.html', list1=list1,
                           list2=list2,
                           list3=list3,
                           list4=list4,
                           list5=list5,
                           list6=list6)


if __name__ == '__main__':
    app.run(debug=True)
