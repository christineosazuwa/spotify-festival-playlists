import requests
import sys
import os
import spotipy
import spotipy.util as util
import spotipy.oauth2
from flask import (Flask, request, redirect, render_template, url_for, session, flash)
from played import festbyyear
from played import match_fest
from time import sleep
import itertools
import time
from time import gmtime, strftime
os.system("played.py 1")

app = Flask(__name__)

CLIENT_SIDE_URL = "CLIENT URL"
PORT = 8080
REDIRECT_URI = "{}/playlists".format(CLIENT_SIDE_URL)
SCOPE = ("playlist-modify-public playlist-modify-private "
         "playlist-read-collaborative playlist-read-private")

def get_oauth():
    """Return a Spotipy Oauth2 object."""
    return spotipy.oauth2.SpotifyOAuth('CLIENT ID', 'CLIENT SECRET KEY', 
                                       REDIRECT_URI, scope=SCOPE, cache_path=".tokens")

def get_spotify(auth_token=None):
    """Return an authenticated Spotify object."""
    oauth = get_oauth()
    token_info = oauth.get_cached_token()
    if not token_info and auth_token:
        token_info = oauth.get_access_token(auth_token)
    return spotipy.Spotify(token_info["access_token"])

def id_search(band):
    sp = get_spotify()
    return sp.search(q=band, limit=1, type='artist')['artists']['items'][0]['id']

def id_search(band):
    sp = get_spotify()
    return sp.search(q=band, limit=1, type='artist')['artists']['items'][0]['id']

def top_track_search(band):
    sp = get_spotify()
    return sp.artist_top_tracks(id_search(band), country='US')['tracks'][0]['id']

def create_playlist(fest1, year):
    sp = get_spotify()
    username = sp.current_user()['id']
    playlist_title = ''.join([match_fest(fest1), ' ', str(year)])
    global new_playlist_id
    new_playlist_id = sp.user_playlist_create(username, playlist_title, public=False).get('id')

def get_tracks(fest1, year, no1, no2):
    sp = get_spotify()
    username = sp.current_user()['id']
    global fest_tracks
    fest_tracks = []
    for band in festbyyear(fest1, year)[no1:no2]:
        sleep(3)
        try:
            fest_tracks.append(top_track_search(band))
        except:
            pass
        
def addtracks():
    sp = get_spotify()
    username = sp.current_user()['id']
    sp.user_playlist_add_tracks(username, new_playlist_id, fest_tracks)
    
def new_playlist(fest1, year):
    sp = get_spotify()
    username = sp.current_user()['id']
    todo = itertools.chain.from_iterable(itertools.repeat(
            [create_playlist(fest1, year), 
             get_tracks(fest1, year, 0, 5), addtracks(), 
             get_tracks(fest1, year, 6, 10), addtracks()],0))
    start = time.time()
    try:
        while time.time() < start + 5:
            todo.next()()
    except:
        pass

# Define a route for the default URL, which loads the form

@app.route("/")
def index():
    """Redirect user to Spotify login/auth."""
    sp_oauth = get_oauth()
    return redirect(sp_oauth.get_authorize_url())
    #return render_template("playlist.html")

@app.route("/playlists")
def form():
    """Render playlists as buttons to choose from."""
    # This is the route which the Spotify OAuth redirects to.
    # We finish getting an access token here.
    if request.args.get("code"):
        get_spotify(request.args["code"])

    return render_template("playlist.html")


@app.route('/hello/', methods=['POST'])
def hello():
    fest1=request.form['fest1']
    year=request.form['year']
    return render_template('playlist_submit.html', fest1=fest1, fest1name=match_fest(fest1), 
                           year=year, playlist=new_playlist(fest1, int(year)))

if __name__ == "__main__":
    app.run(port=PORT)