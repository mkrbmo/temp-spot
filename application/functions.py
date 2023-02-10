import random, string, requests, time, base64, json
from flask import redirect, session
from flask import current_app as app


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
INPUT:
EMOTION
"""
def analyze_sentiment(sentence):
    emotion = app.pipe(sentence)[0][0]['label']
    conversions = {'admiration': {'energy': 'mid', 'valence': 'high', 'genre': ['alternative', ' happy', ' indie', ' pop']}, 'amusement': {'energy': 'mid', 'valence': 'mid', 'genre': ['happy', ' summer', ' electronic']}, 'anger': {'energy': 'high', 'valence': 'low', 'genre': ['punk rock', ' grunge', ' hard rock']}, 'annoyance': {'energy': 'low', 'valence': 'low', 'genre': ['industrial', ' ambient']}, 'approval': {'energy': 'mid', 'valence': 'mid', 'genre': ['acoustic', ' chill', ' progressive']}, 'caring': {'energy': 'low', 'valence': 'high', 'genre': ['singer-songwriter', ' songwriter']}, 'confusion': {'energy': 'low', 'valence': 'mid', 'genre': ['electro', ' industrial', ' trance']}, 'curiosity': {'energy': 'mid', 'valence': 'mid', 'genre': ['deep-house', ' progressive-house']}, 'desire': {'energy': 'low', 'valence': 'high', 'genre': ['romance', ' piano']}, 'disappointment': {'energy': 'low', 'valence': 'low', 'genre': ['sad', ' piano', ' guitar']}, 'disapproval': {'energy': 'low', 'valence': 'low', 'genre': ['sad', ' piano', ' guitar']}, 'disgust': {'energy': 'mid', 'valence': 'low', 'genre': ['ambient', ' sad', ' grunge']}, 'embarrassment': {'energy': 'low', 'valence': 'low', 'genre': ['industrial', ' minimal-techno']}, 'excitement': {'energy': 'high', 'valence': 'high', 'genre': ['party', ' edm']}, 'fear': {'energy': 'high', 'valence': 'low', 'genre': ['industrial', ' grunge']}, 'gratitude': {'energy': 'low', 'valence': 'high', 'genre': ['happy', ' summer', ' chill']}, 'grief': {'energy': 'low', 'valence': 'low', 'genre': ['sad', ' piano', ' guitar']}, 'joy': {'energy': 'high', 'valence': 'high', 'genre': ['synth-pop', ' power-pop']}, 'love': {'energy': 'low', 'valence': 'high', 'genre': ['romance', ' r-n-b']}, 'nervousness': {'energy': 'high', 'valence': 'low', 'genre': ['industrial', ' trance']}, 'optimism': {'energy': 'mid', 'valence': 'high', 'genre': ['happy', ' new-age']}, 'pride': {'energy': 'high', 'valence': 'high', 'genre': ['party', ' happy', ' new-age']}, 'realization': {'energy': 'mid', 'valence': 'mid', 'genre': ['ambient', ' study']}, 'relief': {'energy': 'mid', 'valence': 'mid', 'genre': ['acoustic', ' chill', ' study']}, 'remorse': {'energy': 'low', 'valence': 'low', 'genre': ['sad', ' piano', ' guitar']}, 'sadness': {'energy': 'low', 'valence': 'low', 'genre': ['sad', ' piano', ' rainy-day']}, 'surprise': {'energy': 'high', 'valence': 'mid', 'genre': ['minimal-techno', ' house']}, 'neutral': {'energy': 'mid', 'valence': 'mid', 'genre': ['world-music', ' chill']}}
    if emotion in conversions:
        return conversions[emotion]



def generate_url(session):

    def parse_level(level):
        if level == 'low':
            return {'min': 0.0, 'max': 0.35}
        elif level == 'mid':
            return{'min': 0.35, 'max': 0.65}
        elif level == 'high':
            return {'min': 0.65, 'max': 1.0}


    limit = session['length'] + 10
    seed = '%2C'.join(x.strip() for x in session['genre'])
    energy = parse_level(session['energy'])
    valence = parse_level(session['valence'])
    instrumentalness = parse_level(session['instrumentalness'])
    popularity = parse_level(session['popularity']) 

    url = f"""https://api.spotify.com/v1/recommendations
            ?limit={limit}
            &market=US
            &seed_genres={seed}
            &min_energy={energy['min']}&max_energy={energy['max']}
            &min_instrumentalness={instrumentalness['min']}&max_instrumentalness={instrumentalness['max']}
            &min_popularity={popularity['min']*100}&max_popularity={popularity['max']*100}
            &min_valence={valence['max']}&max_valence={valence['max']}
        """

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
    response_tracks = response.json()['tracks']
    tracks = {track['uri']:clean_track(track) for track in response_tracks}

    return tracks

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
    
