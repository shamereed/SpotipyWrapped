from flask import Flask, render_template
import spotipy_requests

app = Flask(__name__)

# Web scraping function (example: scrape quotes from a site)
def scrape_data_artists(term):
    topArtistST = spotipy_requests.getCurrentUserTopArtists(term)
    
    return topArtistST
    
# Web scraping function (example: scrape quotes from a site)
def scrape_data_tracks(term):
    topTrackST = spotipy_requests.getCurrentUserTopTracks(term)
    
    return topTrackST

@app.route('/')
def home():
    #list1 = scrape_data_artists('short')  # Scrape data when accessing the home page
    #list2 = scrape_data_artists('medium')
    #list3 = scrape_data_artists('long')
    #list4 = scrape_data_tracks('short')  # Scrape data when accessing the home page
    #list5 = scrape_data_tracks('medium')
    #list6 = scrape_data_tracks('long')
    #return render_template('index.html',  list1=list1, list2=list2, list3=list3, list4=list4, list5=list5, list6=list6)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)