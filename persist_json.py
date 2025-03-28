import json
import sqlite3
import datetime

# Define file paths

current_datetime = datetime.datetime.now()
current_time_str = current_datetime.strftime("%Y%m%d")

DB_FILE = ".db"
ARTISTS_TABLE_NAME = "artists"
TRACKS_TABLE_NAME = "tracks"


def create_table_tracks(conn):
    """
    Creates an SQLite table for storing track data.
    """
    cursor = conn.cursor()

    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {TRACKS_TABLE_NAME} (
        id TEXT PRIMARY KEY,
        name TEXT,
        artist TEXT,
        album TEXT,
        album_release_date TEXT,
        duration_ms INTEGER,
        popularity INTEGER,
        explicit INTEGER,
        spotify_url TEXT,
        album_image_url TEXT,
        time_range TEXT,
        update_date TEXT
    )
    """
    cursor.execute(create_table_query)
    conn.commit()


def create_table_artists(conn):
    """
    Creates an SQLite table for storing artist data.
    """
    cursor = conn.cursor()

    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {ARTISTS_TABLE_NAME} (
        id TEXT PRIMARY KEY,
        name TEXT,
        popularity INTEGER,
        followers INTEGER,
        genres TEXT,
        spotify_url TEXT,
        image_url TEXT,
        time_range TEXT,
        update_date TEXT
    )
    """
    cursor.execute(create_table_query)
    conn.commit()


def insert_data_tracks(json_data, conn, term):
    """
    Inserts JSON data into the SQLite table.
    """
    cursor = conn.cursor()

    insert_query = f"""
    INSERT OR IGNORE INTO {TRACKS_TABLE_NAME} 
    (id, name, artist, album, album_release_date, duration_ms, popularity, explicit, spotify_url, album_image_url, time_range, update_date) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    for track in json_data:
        track_id = track.get("id")
        name = track.get("name")
        artist = ", ".join([artist["name"] for artist in track.get("artists", [])])
        album = track.get("album", {}).get("name", "")
        album_release_date = track.get("album", {}).get("release_date", "")
        duration_ms = track.get("duration_ms", 0)
        popularity = track.get("popularity", 0)
        explicit = int(track.get("explicit", False))  # Convert Boolean to Integer (0/1)
        spotify_url = track.get("external_urls", {}).get("spotify", "")
        album_image_url = track.get("album", {}).get("images", [{}])[0].get("url", "")
        time_range = term
        update_date = current_time_str

        cursor.execute(insert_query, (track_id, name, artist, album, album_release_date, duration_ms, popularity, explicit, spotify_url, album_image_url, time_range, update_date))

    conn.commit()


def insert_data_artists(json_data, conn, term):
    """
    Inserts JSON data into the SQLite table.
    """
    cursor = conn.cursor()

    insert_query = f"""
    INSERT OR IGNORE INTO {ARTISTS_TABLE_NAME} 
    (id, name, popularity, followers, genres, spotify_url, image_url, time_range, update_date) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    for artist in json_data:
        artist_id = artist.get("id")
        name = artist.get("name")
        popularity = artist.get("popularity", 0)
        followers = artist.get("followers", {}).get("total", 0)
        genres = ", ".join(artist.get("genres", []))  # Convert list to a string
        spotify_url = artist.get("external_urls", {}).get("spotify", "")
        image_url = artist.get("images", [{}])[0].get("url", "")  # Get the first image
        time_range = term
        update_date = current_time_str

        cursor.execute(insert_query, (
            artist_id, name, popularity, followers, genres, spotify_url, image_url, time_range, update_date))

    conn.commit()


def fetch_and_display_data_tracks(conn):
    """
    Fetches and displays the stored data.
    """
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {TRACKS_TABLE_NAME} LIMIT 25")
    rows = cursor.fetchall()

    for row in rows:
        print(row)


def fetch_and_display_data_artists(conn):
    """
    Fetches and displays the stored data.
    """
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {ARTISTS_TABLE_NAME} LIMIT 25")
    rows = cursor.fetchall()

    for row in rows:
        print(row)


def persistJsonTracks(json_path, type_of_req, term):
    # Load JSON data from the file
    with open(json_path, "r", encoding="utf-8") as file:
        json_data = json.load(file)

    # Connect to SQLite database
    conn = sqlite3.connect(type_of_req + DB_FILE)

    # Create table and insert data
    create_table_tracks(conn)
    insert_data_tracks(json_data, conn, term)

    print("Data successfully inserted into the SQLite database!")

    # Fetch and display stored data
    fetch_and_display_data_tracks(conn)

    # Close database connection
    conn.close()


def persistJsonArtists(json_path, type_of_req, term):
    # Load JSON data from the file
    with open(json_path, "r", encoding="utf-8") as file:
        json_data = json.load(file)

    # Connect to SQLite database
    conn = sqlite3.connect(type_of_req + DB_FILE)

    # Create table and insert data
    create_table_artists(conn)
    insert_data_artists(json_data, conn, term)

    print("Data successfully inserted into the SQLite database!")

    # Fetch and display stored data
    fetch_and_display_data_artists(conn)

    # Close database connection
    conn.close()
