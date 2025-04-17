from flask import Flask, render_template
import spotipy_requests
import cache_token

# Authenticate spotify account
sp = cache_token.authenticate_spotify()
app = Flask(__name__)


def __init__():
    app.static_folder = 'static'


# returns top items json object : top_items_sorted,
# sorted list of top items : top_items
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

    return render_template('index.html', list1=list1[0],
                           list2=list2[0],
                           list3=list3[0],
                           list4=list4[0],
                           list5=list5[0],
                           list6=list6[0])


@app.route('/persist')
def persistJson():
    list1 = scrape_data('artists', 'short')
    list2 = scrape_data('artists', 'medium')
    list3 = scrape_data('artists', 'long')
    list4 = scrape_data('tracks', 'short')
    list5 = scrape_data('tracks', 'medium')
    list6 = scrape_data('tracks', 'long')

    spotipy_requests.writeResultsToJson(list1[1], 'artists', 'short')
    spotipy_requests.writeResultsToJson(list2[1], 'artists', 'medium')
    spotipy_requests.writeResultsToJson(list3[1], 'artists', 'long')
    spotipy_requests.writeResultsToJson(list4[1], 'tracks', 'short')
    spotipy_requests.writeResultsToJson(list5[1], 'tracks', 'medium')
    spotipy_requests.writeResultsToJson(list6[1], 'tracks', 'long')

    return render_template('index.html', list1=list1[0],
                           list2=list2[0],
                           list3=list3[0],
                           list4=list4[0],
                           list5=list5[0],
                           list6=list6[0])


if __name__ == '__main__':
    app.run(debug=True)
