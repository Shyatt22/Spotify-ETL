# Spotify ETL

## ETL
I did ETL using Spotify's Spotipy API. You can find your client ID and Client Secret here (https://developer.spotify.com/console/get-recently-played/). The data consists of 50 recently played songs and a user ID, which are put into a Pandas dataframe. Then, the data is validated to check whether the dataset is empty, has any nulls, or the primary key is violated. After that, a table is created and the data is loaded into a SQLite database.
