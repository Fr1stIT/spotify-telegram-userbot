
import spotipy
import spotipy.util as util
from pyrogram import Client, filters
import time

import requests


api_id = 'YOUR API ID (int)'
api_hash = "YOUR API HASH (str)"
app = Client("my_account", api_id=api_id, api_hash=api_hash)


# Записываем в переменные:
CLIENT_ID = 'xxx' # client ID
CLIENT_SECRET = 'xxx' # client secret
rur = 'xxx' # redirected URI
user = 'xxx' # имя пользователя
username = user
scope = "user-read-currently-playing"
redirect_uri = "xxx"




def main():
    with app:
        while True:

            token = util.prompt_for_user_token(username, scope, CLIENT_ID, CLIENT_SECRET, redirect_uri)

            sp = spotipy.Spotify(auth=token)
            currentsong = sp.currently_playing()


            if currentsong == None:

                anw = ("Сейчас ничего не играет :(")  #if no to play
                print(anw)
                app.update_profile(first_name="Frist", bio=anw)
                time.sleep(120)

            else:
                song_name = currentsong['item']['name']
                song_artist = currentsong['item']['artists'][0]['name']
                anw = ("Сейчас играет:  {} | {}".format(song_name, song_artist))
                url = currentsong["item"]["album"]["images"][0]["url"]
                r = requests.get(url)
                with open(f'./img/{song_name}-{song_artist}.jpg', 'wb') as f:
                    f.write(r.content)  # Retrieve HTTP meta-data


                app.update_profile(first_name="Frist", bio=anw)
                print(anw)

                app.set_profile_photo(photo=f'./img/{song_name}-{song_artist}.jpg')

                # Get the photos to be deleted
                photos = []
                for p in app.get_chat_photos("me"):
                    photos.append(p)

                # Delete the rest of the photos
                app.delete_profile_photos([p.file_id for p in photos[1:]])

                time.sleep(50)




@app.on_message(filters.command('song', prefixes='.') & filters.me)
def song(_, message):
    token = util.prompt_for_user_token(username, scope, CLIENT_ID, CLIENT_SECRET, redirect_uri)

    sp = spotipy.Spotify(auth=token)
    currentsong1 = sp.currently_playing()
    song_name1 = currentsong1['item']['name']

    song_artist1 = currentsong1['item']['artists'][0]['name']
    anw1 = ("Послушай со мной {} | {}".format(song_name1, song_artist1))  #command .song
    message.edit(text=anw1)




app.run(main())

