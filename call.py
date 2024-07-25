from dotenv import load_dotenv
import os
import base64
import json
from requests import post,get
import random

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes),"utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def get_seeds(token, mood, seedTracks, seedArtists):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={mood}&type=track&limit=5"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["tracks"]["items"]

    for item in json_result:
        seedTracks.append(item["id"])


def get_recommendation(token, seedTracks):
    url = "https://api.spotify.com/v1/recommendations"
    headers = get_auth_header(token)

    track = random.choice(seedTracks)
    query = f"?limit=5&seed_tracks={track}"
    query_url = url + query
    
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["tracks"]

    track = random.choice(json_result);

    song_img_src = track["album"]["images"][2]["url"]
    song_url = track["external_urls"]["spotify"]
    song_name = track["name"]
    song_artist = track["artists"][0]["name"]
    
    song = [song_name, song_artist, song_url, song_img_src]
    return song







