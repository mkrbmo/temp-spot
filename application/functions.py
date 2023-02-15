import random, string, requests, time, base64, json
from flask import redirect, session
from flask import current_app as app
from application import pipe


"""
argument: client session
returns: access token if not expired; refresh token if successfully refreshed; redirect to authorize if failure
purpose: confirmed token hasn't expired before making request to spotify api
"""
def check_token(session):
    if 'access_token' not in session:
        return redirect('/authorize')
    elif session['expiration'] < time.time():
        response = refresh_token(session['refresh_token'])
        if response == None:
            #ADD REDIRECT URL
            return redirect('/authorize')
        else:
            session['access_token'] = response['access_token']
            session['expiration'] = time.time() + response['expires_in']
            return None
    return None

"""
argument: refresh token from session
returns: json object containing access token and expiration; None if failure
purpose: refreshes access token from spotify api using refresh token
"""
def refresh_token(token):
    #code = request.args.get('code')
    authString = app.config['SPOTIFY_CLIENT_ID']+':'+ app.config['SPOTIFY_SECRET']
    b64AuthString = base64.urlsafe_b64encode(authString.encode()).decode()

    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': "Basic " + b64AuthString, 
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    body = {
        'refresh_token': token,
        'grant_type': 'authorization_code',
    }
    response = requests.post(url, headers=headers, data=body)

    if response.status_code != 200:
        print('Error:', response.status_code)
        return None 
    else:
        json_response = response.json()
        return json_response
    

def generate_key(length):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))

"""
INPUT: USER PROVIDED SENTENCE
RETURNS: DICITONARY OF AUDIO FEATURES AND GENRES
"""
def analyze_sentiment(sentence):
    emotion = pipe(sentence)[0][0]['label']
    conversions = {'admiration': {'min_valence': 0.65, 'max_valence': 1.0, 'min_energy': 0.35, 'max_energy': 0.65, 'genre': 'alternative, happy, indie, pop'}, 'amusement': {'min_valence': 0.35, 'max_valence': 0.65, 'min_energy': 0.35, 'max_energy': 0.65, 'genre': 'happy, summer, electronic'}, 'anger': {'min_valence': 0.0, 'max_valence': 0.35, 'min_energy': 0.65, 'max_energy': 1.0, 'genre': 'punk rock, grunge, hard rock'}, 'annoyance': {'min_valence': 0.0, 'max_valence': 0.35, 'min_energy': 0.0, 'max_energy': 0.35, 'genre': 'industrial, ambient'}, 'approval': {'min_valence': 0.35, 'max_valence': 0.65, 'min_energy': 0.35, 'max_energy': 0.65, 'genre': 'acoustic, chill, progressive'}, 'caring': {'min_valence': 0.65, 'max_valence': 1.0, 'min_energy': 0.0, 'max_energy': 0.35, 'genre': 'singer-songwriter, songwriter'}, 'confusion': {'min_valence': 0.35, 'max_valence': 0.65, 'min_energy': 0.0, 'max_energy': 0.35, 'genre': 'electro, industrial, trance'}, 'curiosity': {'min_valence': 0.35, 'max_valence': 0.65, 'min_energy': 0.35, 'max_energy': 0.65, 'genre': 'deep-house, progressive-house'}, 'desire': {'min_valence': 0.65, 'max_valence': 1.0, 'min_energy': 0.0, 'max_energy': 0.35, 'genre': 'romance, piano'}, 'disappointment': {'min_valence': 0.0, 'max_valence': 0.35, 'min_energy': 0.0, 'max_energy': 0.35, 'genre': 'sad, piano, guitar'}, 'disapproval': {'min_valence': 0.0, 'max_valence': 0.35, 'min_energy': 0.0, 'max_energy': 0.35, 'genre': 'sad, piano, guitar'}, 'disgust': {'min_valence': 0.0, 'max_valence': 0.35, 'min_energy': 0.35, 'max_energy': 0.65, 'genre': 'ambient, sad, grunge'}, 'embarrassment': {'min_valence': 0.0, 'max_valence': 0.35, 'min_energy': 0.0, 'max_energy': 0.35, 'genre': 'industrial, minimal-techno'}, 'excitement': {'min_valence': 0.65, 'max_valence': 1.0, 'min_energy': 0.65, 'max_energy': 1.0, 'genre': 'party, edm'}, 'fear': {'min_valence': 0.0, 'max_valence': 0.35, 'min_energy': 0.65, 'max_energy': 1.0, 'genre': 'industrial, grunge'}, 'gratitude': {'min_valence': 0.65, 'max_valence': 1.0, 'min_energy': 0.0, 'max_energy': 0.35, 'genre': 'happy, summer, chill'}, 'grief': {'min_valence': 0.0, 'max_valence': 0.35, 'min_energy': 0.0, 'max_energy': 0.35, 'genre': 'sad, piano, guitar'}, 'joy': {'min_valence': 0.65, 'max_valence': 1.0, 'min_energy': 0.65, 'max_energy': 1.0, 'genre': 'synth-pop, power-pop'}, 'love': {'min_valence': 0.65, 'max_valence': 1.0, 'min_energy': 0.0, 'max_energy': 0.35, 'genre': 'romance, r-n-b'}, 'nervousness': {'min_valence': 0.0, 'max_valence': 0.35, 'min_energy': 0.65, 'max_energy': 1.0, 'genre': 'industrial, trance'}, 'optimism': {'min_valence': 0.65, 'max_valence': 1.0, 'min_energy': 0.35, 'max_energy': 0.65, 'genre': 'happy, new-age'}, 'pride': {'min_valence': 0.65, 'max_valence': 1.0, 'min_energy': 0.65, 'max_energy': 1.0, 'genre': 'party, happy, new-age'}, 'realization': {'min_valence': 0.35, 'max_valence': 0.65, 'min_energy': 0.35, 'max_energy': 0.65, 'genre': 'ambient, study'}, 'relief': {'min_valence': 0.35, 'max_valence': 0.65, 'min_energy': 0.35, 'max_energy': 0.65, 'genre': 'acoustic, chill, study'}, 'remorse': {'min_valence': 0.0, 'max_valence': 0.35, 'min_energy': 0.0, 'max_energy': 0.35, 'genre': 'sad, piano, guitar'}, 'sadness': {'min_valence': 0.0, 'max_valence': 0.35, 'min_energy': 0.0, 'max_energy': 0.35, 'genre': 'sad, piano, rainy-day'}, 'surprise': {'min_valence': 0.35, 'max_valence': 0.65, 'min_energy': 0.65, 'max_energy': 1.0, 'genre': 'minimal-techno, house'}, 'neutral': {'min_valence': 0.35, 'max_valence': 0.65, 'min_energy': 0.35, 'max_energy': 0.65, 'genre': 'world-music, chill'}}
    if emotion in conversions:
        return conversions[emotion]



def generate_url(features):

    limit = int(features['length']) + 10
    seed = features['genre'].replace(', ','%2C')
    
    

    url = f"https://api.spotify.com/v1/recommendations?limit={limit}&market=US&seed_genres={seed}&max-popularity=0.5"
    
    for feature, value in features.items():
        if feature == 'length' or feature == 'genre':
            continue

        url += ('&'+feature+"="+str(value))
        
    return url

"""
INPUT: SINGLE TRACK DICTIONARY FROM SPOTIFY API
OUTPUT: CLEANED DICTIONARY 
"""
def clean_track(track):
    output = {}
    output['album'] = track['album']['name']
    output['artists'] = ', '.join([artist['name'] for artist in track['artists']])
    output['title'] = track['name']
    output['cover_url'] = track['album']['images'][2]['url'] #index two specifies small image size
    output['preview_url'] = track['preview_url']
    output['uri'] = track['uri']
    output['track_url'] = track['external_urls']['spotify']

    return output

"""
INPUT: URL FOR FETCHING RECCOMENDATION FROM SPOTIFY API
OUTPUT: DICTIONARY OF TRACKS WITH FORMAT "URL: TRACK DICT"
"""
def get_tracks(url):
    headers = {
            'Authorization': 'Bearer ' + session['access_token'],
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        response_tracks = response.json()['tracks']
        tracks = {track['uri']:clean_track(track) for track in response_tracks}

        return tracks
    print(response.status_code)
    return None


def populate_tracks(sentence):
    features = analyze_sentiment(sentence)
    for feature in features:
        session['features'][feature] = features[feature]
    
    url = generate_url(session['features'])
    session['current_url'] = url
    print(url)
    tracks = get_tracks(url)
    
    if tracks == None:
        return None

    #arbitrary separation of first 10 tracks by URI
    keys = [_ for _ in tracks.keys()]
    current = keys[:session['features']['length']]
    queued = keys[session['features']['length']:]

    session['all_tracks'] = keys
    session['current_tracks'] = {k:tracks[k] for k in current}
    #print(session['current_tracks'])
    session['queued_tracks'] = {k:tracks[k] for k in queued}
    session['queued_keys'] = queued

    return session['current_tracks']



def get_user():
    url = "https://api.spotify.com/v1/me"
    headers = {
            'Authorization': 'Bearer ' + session['access_token'],
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    response = requests.get(url, headers=headers)
    
    return response


def create_playlist(user_id, name, description, public):
    url = f'https://api.spotify.com/v1/users/{user_id}/playlists'
    
    headers = {
            'Authorization': 'Bearer ' + session['access_token'],
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    body = {
        "name": f"{name}",
        "description": f"{description}",
        "public": False
    }
    response = requests.post(url, headers=headers, data=json.dumps(body))
    
    return response
    

def populate_playlist(playlist_id):
    print(session['current_tracks'].keys())
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {
            'Authorization': 'Bearer ' + session['access_token'],
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    body = {
        "uris": list(session['current_tracks'].keys())
    }
    print(session['current_tracks'].keys())
    response = requests.post(url, headers=headers, data=json.dumps(body))

    return response
    
