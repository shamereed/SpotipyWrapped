from timeit import default_timer as timer

import datetime
import json
import persist_json


def getTopGenres(sp, term):
    start = timer()
    listOfGenres = []
    results = sp.current_user_top_artists(limit=50, offset=0, time_range=term + '_term')
    for item in results['items']:
        for genre in item['genres']:
            listOfGenres.append(genre)

    most_frequent = sorted(set(listOfGenres), key=listOfGenres.count, reverse=True)
    print(most_frequent)
    most_frequent_sorted = []
    x = 1
    for genre in most_frequent:
        most_frequent_sorted.append(str(x) + ". " + genre.title())
        x = x + 1

    elapsed_time = timer() - start
    print(elapsed_time)
    return most_frequent_sorted


def getCurrentUserTopItems(sp, type_of_req, term):
    start = timer()
    results = []
    if type_of_req == 'tracks':
        results = sp.current_user_top_tracks(limit=50, offset=0, time_range=term + '_term')
    else:
        results = sp.current_user_top_artists(limit=50, offset=0, time_range=term + '_term')
    top_items = results['items']

    top_items_sorted = []

    x = 1
    for item in top_items:
        if x < 51:
            if type_of_req == 'tracks':
                top_items_sorted.append(
                    str(x) + ". " + item['name'] + " - " + item['artists'][0]['name'] + " - " + item['album'][
                                                                                                    'release_date'][:4])
            else:
                top_items_sorted.append(str(x) + ". " + item['name'])
            x += 1

    elapsed_time = timer() - start
    print(elapsed_time)
    return top_items_sorted, top_items


def writeResultsToJson(top_items, type_of_req, term):
    current_datetime = datetime.datetime.now()
    current_time_str = current_datetime.strftime("%Y%m%d")
    file_path = "json/" + type_of_req + "/" + type_of_req + "_" + term + "_term" + current_time_str + ".json"
    with open(file_path, "w") as json_file:
        json.dump(top_items, json_file, indent=4)
    if type_of_req == 'tracks':
        persist_json.persistJsonTracks(file_path, type_of_req, term)
    else:
        persist_json.persistJsonArtists(file_path, type_of_req, term)
