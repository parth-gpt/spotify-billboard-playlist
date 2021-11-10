import requests as requests
from bs4 import BeautifulSoup
import lxml
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = {}
CLIENT_SECRET = {}
REDIRECT_URI = {}

# Extracting Top 100 Songs
date = input("Which year do you wanna travel to? Type the date in this format YYYY-MM-DD: ")

URL = f"https://www.billboard.com/charts/hot-100/{date}"

response = requests.get(URL)
page = response.text

soup = BeautifulSoup(page, "lxml")

songs = soup.find_all(name="span", class_="chart-element__information__song")
songs_list = []
for song in songs:
    songs_list.append(song.get_text())
# print(songs_list)

# Adding songs to Spotify Playlist

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope="playlist-modify-private",
                                               show_dialog=True,
                                               cache_path="token.txt"))
user_id = sp.current_user()["id"]

song_uris = []

year = date.split("-")[0]
for song in songs_list:
    result = sp.search(q=f"track:{song} year={year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
        # print(result)
    except:
        print(f"{song} is not available in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, public=False, name=f"{date} Billboard")
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
