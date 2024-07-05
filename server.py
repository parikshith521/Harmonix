from flask import Flask, request, render_template
from flask_cors import CORS
import call
#mport mood

import requests
from bs4 import BeautifulSoup
from happytransformer import HappyTextClassification




app = Flask(__name__)
CORS(app)



@app.route('/', methods=['POST'])
def handle_data():



    data = request.get_json()

    print("DATA RECEIVED: ")
    print(data)

    happy_model=HappyTextClassification(model_type='Distilbert',model_name='bhadresh-savani/distilbert-base-uncased-emotion',num_labels=6)


    finaltext = ""

    for url in data:
        url = data[0]
        r = requests.get(url)
        html_doc = r.text
        soup=BeautifulSoup(html_doc,"html.parser")
        text=soup.get_text()
  

    pred = happy_model.classify_text(finaltext)
    usermood =  pred.label

    print(usermood)
    
    token = call.get_token()
    seedTracks = []
    seedArtists = []

    call.get_seeds(token, usermood, seedTracks, seedArtists)

    song = call.get_recommendation(token,seedTracks,seedArtists)

    print(song)

    return song

    

if __name__ == '__main__':
    app.run(port=8080)
