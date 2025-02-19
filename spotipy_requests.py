import spotipy
from timeit import default_timer as timer


def getCurrentUserTopItems(sp, type_of_req, term):
    start = timer()
    results = []
    if type_of_req == 'tracks':
        results = sp.current_user_top_tracks(limit=25, offset=0, time_range=term + '_term')
    else:
        results = sp.current_user_top_artists(limit=25, offset=0, time_range=term + '_term')
    topItems = results['items']
    x = 1
    while results['next']:
        results = sp.next(results)
        topItems.extend(results['items'])

    topItemsSorted = []

    x = 1
    for item in topItems:
        if x < 26:
            if type_of_req == 'tracks':
                topItemsSorted.append(str(x) + ". " + item['name'] + " - " + item['artists'][0]['name'])
            else:
                topItemsSorted.append(str(x) + ". " + item['name'])
            x += 1

    elapsed_time = timer() - start
    print(elapsed_time)
    return topItemsSorted
