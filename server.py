from flask import Flask, request
from flask_cors import CORS
import call
import llm_interact_v3

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST'])
def handle_data():

    data = request.get_json()
    usermood = llm_interact_v3.song_retrieve(data)

    token = call.get_token()
    seedTracks, seedArtists = [], []

    call.get_seeds(token, usermood, seedTracks, seedArtists)
    song = call.get_recommendation(token,seedTracks)
    return song

if __name__ == '__main__':
    app.run(port=llm_interact_v3.os.getenv('PORT'))
