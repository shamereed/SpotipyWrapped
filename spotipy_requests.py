import spotipy
from spotipy.oauth2 import SpotifyOAuth
import configparser
import os
    
config = configparser.ConfigParser()
config_file_path = os.path.join(os.path.dirname(__file__), 'config.cfg')

config.read(config_file_path)
client_id = config.get('api_keys', 'client_id')
client_secret = config.get('api_keys', 'client_secret')
redirect_uri = config.get('api_keys', 'redirect_uri')

print(client_id)
print(client_secret)
print(redirect_uri)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id,
                                               client_secret,
                                               redirect_uri,
                                               scope="user-read-recently-played, user-top-read"))


def getCurrentUserTopArtists(term) :
    results = sp.current_user_top_artists(limit=25, offset=0,time_range=term+'_term')
    topArtists = results['items']
    while results['next']:
        results = sp.next(results)
        topArtists.extend(results['items'])
    
    topArtistSorted = []
    
    x = 1
    for artist in topArtists:
        if(x<26):
            topArtistSorted.append(artist['name'])
            x += 1
        
    
    return topArtistSorted

def getCurrentUserTopTracks(term) :
    results = sp.current_user_top_tracks(limit=25, offset=0,time_range=term+'_term')
    topTracks = results['items']
    while results['next']:
        results = sp.next(results)
        topTracks.extend(results['items'])
    
    topTracksSorted = []
    
    x = 1
    for track in topTracks:
        if(x<26):
            topTracksSorted.append(track['name'] + " - " + track['artists'][0]['name'])
            x += 1
        
    
    return topTracksSorted
   