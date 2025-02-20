import configparser
import os
import json
import spotipy
from datetime import datetime, timedelta
from spotipy.oauth2 import SpotifyOAuth

config = configparser.ConfigParser()
config_file_path = os.path.join(os.path.dirname(__file__), 'config.cfg')

config.read(config_file_path)

# Spotify API credentials
CLIENT_ID_CONFIG = config.get('api_keys', 'client_id')
CLIENT_SECRET_CONFIG = config.get('api_keys', 'client_secret')
REDIRECT_URI_CONFIG = config.get('api_keys', 'redirect_uri')
SCOPE_CONFIG = 'user-library-read,user-top-read'

# Token cache file path
TOKEN_CACHE_PATH = 'token_cache.json'

sp_oauth = SpotifyOAuth(client_id=CLIENT_ID_CONFIG,
                        client_secret=CLIENT_SECRET_CONFIG,
                        redirect_uri=REDIRECT_URI_CONFIG,
                        scope=SCOPE_CONFIG,
                        open_browser=True)

print(sp_oauth.get_authorize_url())


def load_token_from_cache():
    """Load cached token from the file if it exists and is valid."""
    if os.path.exists(TOKEN_CACHE_PATH):
        with open(TOKEN_CACHE_PATH, 'r') as file:
            token_info = json.loads(file.read())

            # Check if token is still valid
            expiration_time = datetime.strptime(token_info['expires_at'], "%Y-%m-%dT%H:%M:%S.%f")
            if expiration_time > datetime.now():
                print("Using cached access token.")
                return token_info

    print("No valid cached token found.")
    return None


def save_token_to_cache(token_info):
    """Save the access token and expiration time to cache."""
    token_info['expires_at'] = (datetime.now() + timedelta(seconds=token_info['expires_in'])).isoformat()
    with open(TOKEN_CACHE_PATH, 'w') as file:
        json.dump(token_info, file)
    print("Access token cached successfully.")


def authenticate_spotify():
    """Authenticate and get a valid access token."""
    token_info = load_token_from_cache()

    if token_info is None:
        # If no valid token in cache, request a new token
        sp_oauth1 = SpotifyOAuth(client_id=CLIENT_ID_CONFIG,
                                 client_secret=CLIENT_SECRET_CONFIG,
                                 redirect_uri=REDIRECT_URI_CONFIG,
                                 scope=SCOPE_CONFIG,
                                 open_browser=True)  # Adjust scope based on your needs

        # Get the token using authorization code flow
        token_info = sp_oauth1.get_access_token(sp_oauth1.get_authorize_url())

        # Cache the token
        save_token_to_cache(token_info)

    # Create Spotipy object with the access token
    sp = spotipy.Spotify(auth=token_info['access_token'])
    return sp
