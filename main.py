from test import api_hash, api_id, CLIENT_ID, CLIENT_SECRET, user
import spotipy
import spotipy.util as util
from pyrogram import Client, filters
import time

import requests


api_id = api_id
api_hash = api_hash
app = Client("my_account", api_id=api_id, api_hash=api_hash)

CLIENT_ID = CLIENT_ID
CLIENT_SECRET = CLIENT_SECRET
rur = 'http://127.0.0.1:9090' # redirected URI
user = user # имя пользователя
username = user
scope = "user-read-currently-playing"
redirect_uri = "http://localhost:8888/callback"



def main():
    boolean = False
    bo = True
    last_song = 'testds'
    nothing_song = True
    global currentsong
    with app:
        while True:
            # try:
                token = util.prompt_for_user_token(username, scope, CLIENT_ID, CLIENT_SECRET, redirect_uri)

                sp = spotipy.Spotify(auth=token)
                currentsong = sp.currently_playing()

                if currentsong == None:
                    bo = False
                    anw = ("Сейчас ничего не играет :(")  # if no to play
                    print(anw)
                    if nothing_song == True:
                        app.update_profile(first_name="Frist", bio=anw)
                        nothing_song = False
                else:
                    boolean = True
                    bo = True
                if bo == True:
                    if currentsong['item']['name'] == last_song:
                        boolean = False



                if bo == True:
                    last_song = currentsong['item']['name']
                    nothing_song = True

                else:
                    last_song = ''


                time.sleep(16)
            #Коментарий



                # try:
                if boolean == True:
                        song_name = currentsong['item']['name']
                        song_artist = currentsong['item']['artists'][0]['name']
                        anw = ("Сейчас играет:  {} | {}".format(song_name, song_artist))
                        url = currentsong["item"]["album"]["images"][0]["url"]
                        r = requests.get(url)
                        with open(f'./img/{song_name}-{song_artist}.jpg', 'wb') as f:
                            f.write(r.content)  # Retrieve HTTP meta-data

                        app.update_profile(first_name="Frist", bio=anw)
                        print(anw) #debug
                        app.set_profile_photo(photo=f'./img/{song_name}-{song_artist}.jpg')

                        # Get the photos to be deleted
                        photos = []
                        for p in app.get_chat_photos("me"):
                            photos.append(p)

                        # Delete the rest of the photos
                        app.delete_profile_photos([p.file_id for p in photos[1:]])

                else:
                        print('Играет та же песня, обновление не будет просходить') #if we havethis song in bio
                # except:
                    # print('Error')








@app.on_message(filters.command('song', prefixes='.') & filters.me)
def song(_, message):
    global currentsong
    song_name1 = currentsong['item']['name']

    song_artist1 = currentsong['item']['artists'][0]['name']
    anw1 = ("Послушай со мной {} | {}".format(song_name1, song_artist1))  #command .song
    message.edit(text=anw1)




app.run(main())

