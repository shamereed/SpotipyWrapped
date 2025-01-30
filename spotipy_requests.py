import spotipy
from spotipy.oauth2 import SpotifyOAuth



sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="2f8c3c2412754c8db4a5808c0ff6d1c7",
                                               client_secret="cd5ca563e4484242b9f9aa5fa3ab6658",
                                               redirect_uri="http://localhost:1234",
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
   