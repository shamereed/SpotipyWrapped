from flask import Flask, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy_requests, cache_token
import configparser
import os
import threading, queue
    
config = configparser.ConfigParser()
config_file_path = os.path.join(os.path.dirname(__file__), 'config.cfg')

config.read(config_file_path)
client_id = config.get('api_keys', 'client_id')
client_secret = config.get('api_keys', 'client_secret')
redirect_uri = config.get('api_keys', 'redirect_uri')

TOKEN_CACHE_PATH = 'token_cache.json'
sp = cache_token.authenticate_spotify()

app = Flask(__name__)

# Web scraping function (example: scrape quotes from a site)
def scrape_data(q, type, term):
    topItems = spotipy_requests.getCurrentUserTopItems(sp,type,term)
    
    q.put(topItems)

@app.route('/')
def home():
    threads = []
    q = queue.Queue()
    thread1 = threading.Thread(target=scrape_data, args=(q,'artists','short'))
    thread2 = threading.Thread(target=scrape_data, args=(q,'artists','medium'))
    thread3 = threading.Thread(target=scrape_data, args=(q,'artists','long'))
    #thread4 = threading.Thread(target=scrape_data, args=(q,'tracks','short'))
    #thread5 = threading.Thread(target=scrape_data, args=(q,'tracks','medium'))
   #thread6 = threading.Thread(target=scrape_data, args=(q,'tracks','long'))
    thread1.start()
    thread2.start()
    thread3.start()
    #thread4.start()
    #thread5.start()
    #thread6.start()
    threads.append(thread1)
    threads.append(thread2)
    threads.append(thread3)
    #threads.append(thread4)
    #threads.append(thread5)
    #threads.append(thread6)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    list1 = q.get() 
    list2 = q.get() 
    list3 = q.get() 
    #list4 = q.get() 
    #list5 = q.get() 
    #list6 = q.get() 
    
    #list1 = scrape_data('artists','short') 
    #list2 = scrape_data('artists','medium')
    #list3 = scrape_data('artists','long')
    #list4 = scrape_data('tracks','short') 
    #list5 = scrape_data('tracks','medium')
    #list6 = scrape_data('tracks','long')
    return render_template('index.html',  list1=list1, 
                                          list2=list2, 
                                          list3=list3) 
                                          #list4=list4, 
                                          #list5=list5, 
                                          #list6=list6)

if __name__ == '__main__':
    app.run(debug=True)