from flask import Flask, request, render_template
from flask_cors import CORS
import call
#mport mood

import requests
#from bs4 import BeautifulSoup
#from happytransformer import HappyTextClassification

from llm_interact_v3 import song_retrieve


app = Flask(__name__)
CORS(app)



@app.route('/', methods=['POST'])
def handle_data():



    data = request.get_json()

    print("DATA RECEIVED: ", data)
  
    usermood = song_retrieve(data)
    
    token = call.get_token()
    seedTracks = []
    seedArtists = []

    call.get_seeds(token, usermood, seedTracks, seedArtists)

    song = call.get_recommendation(token,seedTracks)

    print(song)

    return song

    

if __name__ == '__main__':
    app.run(port=8080)
