import json
import requests
from app import app 
from flask import render_template, request, redirect, url_for
from pprint import pprint


# global variables 
access_token = "" 
spotify_url_endpoint = "https://api.spotify.com/v1/me/player/currently-playing"
json_object = None 


@app.route("/", methods=['GET','POST'])
def index(): 
    global access_token, json_object
    if request.method == "POST": 
        access_token = request.form.get("access_token")
        json_object = get_current_track_json(access_token)
        return redirect(url_for('preview')) 
    else: 
        return render_template("index.html")


@app.route("/preview")
def preview(): 
    global json_object
    song_name = json_object["item"]["name"]
    artists = json_object["item"]["artists"]
    album = json_object["item"]["album"]["album_type"]
    # should learn to better use list comprehension 
    song_artists = ", ".join([artist['name'] for artist in artists])
    return render_template("preview.html", artists=song_artists, album=album, song_name=song_name)


# functions 

# function that returns a json object of the response returned by the spotify server 
def get_current_track_json(spotify_access_token):
    global spotify_url_endpoint
    response = requests.get(spotify_url_endpoint, 
                headers={"Authorization": f"Bearer {spotify_access_token}"}   
               )
    json_object = response.json()
    return json_object

