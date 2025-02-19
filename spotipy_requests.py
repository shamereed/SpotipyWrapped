from timeit import default_timer as timer

import datetime
import json


def getCurrentUserTopItems(sp, type_of_req, term):
    start = timer()
    results = []
    if type_of_req == 'tracks':
        results = sp.current_user_top_tracks(limit=25, offset=0, time_range=term + '_term')
    else:
        results = sp.current_user_top_artists(limit=25, offset=0, time_range=term + '_term')
    top_items = results['items']

    writeResultsToJson(sp, top_items, type_of_req, term)

    top_items_sorted = []

    x = 1
    for item in top_items:
        if x < 26:
            if type_of_req == 'tracks':
                top_items_sorted.append(str(x) + ". " + item['name'] + " - " + item['artists'][0]['name'])
            else:
                top_items_sorted.append(str(x) + ". " + item['name'])
            x += 1

    elapsed_time = timer() - start
    print(elapsed_time)
    return top_items_sorted


def writeResultsToJson(sp, top_items, type_of_req, term):
    current_datetime = datetime.datetime.now()
    current_time_str = current_datetime.strftime("%Y%m%d")
    file_path = "json/" + type_of_req + "/" + type_of_req + "_" + term + "_term" + current_time_str + ".json"

    with open(file_path, "w") as json_file:
        json.dump(top_items, json_file, indent=4)
