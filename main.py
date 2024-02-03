from dotenv import load_dotenv
import os
import base64
from requests import post  , get
import json
import math

load_dotenv()

client_id = "880e0d8e2efe4db391bfeccfbe5cb975" #os.getenv("CLIENT_ID")
client_secret = "ed068c230f014d4680c0a1b4d17cf112"#os.getenv("CLIENT_SECRET")


def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes) , "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,  # Added space after Basic
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type" : "client_credentials"}
    result = post(url, headers=headers, data=data)
    
    try:
        json_result = result.json()
        token = json_result.get("access_token")
        if token is None:
            print("Error: 'access_token' not found in API response:", json_result)
            exit()
        return token
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        print("Response content:", result.content)
        exit()


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    
    query_url = url + query
    result = get(query_url,headers = headers)
    json_result = json.loads(result.content)["artists"]["items"]
    #print(json_result)
    
    if len(json_result) == 0 :
        print("No artist with this name exists...")
        return None
    return json_result[0]

def get_songs_by_artist(token,artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url , headers = headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result



token = get_token()
result = search_for_artist(token,"backstreeet boys")
#print(token)

artist_id = result["id"]
songs = get_songs_by_artist(token,artist_id)
#print(songs['name'])
#print(result["name"])

for idx , song in enumerate(songs):
    print(f"{idx + 1}. {song['name']}")



