import spotipy
from spotipy.oauth2 import SpotifyOAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="Your_Client_ID_Here",
                                               client_secret="Your_Client_Secret_Here",
                                               redirect_uri="http://localhost:8080/",
                                               scope="user-read-recently-played, user-read-email"))

results = sp.current_user_recently_played()
user=sp.current_user()

print(results)