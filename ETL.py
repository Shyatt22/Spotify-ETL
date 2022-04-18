import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime
import sqlite3
import spotipy
import random
from Setup import Auth

#SQLite DB setup
DATABASE_LOCATION = "sqlite:///top10.sqlite"

#Data validation function to check for important possible trasnformations
def check_if_valid_data(df: pd.DataFrame)->bool:
    if df.empty:
        print('No songs downloaded. Finishing execution.')
        return False

    if pd.Series(df['played_at']).is_unique:
        pass
    else:
        raise Exception('Primary key is violated')

    if df.isnull().values.any():
        raise Exception('Null values found')


def main():
    #Extracts authorized data into this file
    listen_data=Auth.results
    user_data=Auth.user
    
    #Takes the ID value from user data
    user_id=(user_data['id'])
    
    user_id_list=[]
    song_names=[]
    artist_names=[]
    played_at_list=[]
    timestamps=[]

    #Brings relevant data into lists
    for song in listen_data["items"]:
        user_id_list.append(user_id)
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at_list.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])
        
    #Collects lists into a dictionary
    song_dict={
        "user_id":user_id_list,
        "song_name":song_names,
        "artist_name":artist_names,
        "played_at":played_at_list,
        "timestamp":timestamps
    }

    #Creates a Pandas dataframe to get data into a tabular format 
    song_df=pd.DataFrame(song_dict,columns=["user_id","song_name","artist_name","played_at","timestamp"])
    
    print(song_df)
    
    #Checks if data needs to be further processed per conditions of data validation function
    if check_if_valid_data(song_df):
        print('Data is valid.')

    #SQLite setup for data loading
    engine=sqlalchemy.create_engine(DATABASE_LOCATION)
    dbconnect=sqlite3.connect('top10.sqlite')
    cursor=dbconnect.cursor()
    
    #Creates table for data
    user_song_table='''
    CREATE TABLE IF NOT EXISTS top10(
        user_id INT(11),
        song_name NVARCHAR(200),
        artist_name NVARCHAR(200),
        played_at VARCHAR(50),
        timestamp VARCHAR(50),
        CONSTRAINT primary_key_constraint PRIMARY KEY (played_at)
        ); 
    '''
    
    #Does data loading
    cursor.execute(user_song_table)
    print("table creation successful")

    try:
        song_df.to_sql("top10", engine, index=False, if_exists='append')
    except:
        print("Data already exists")

    dbconnect.close()
if __name__ == '__main__':
    main()
