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


def initialize_session():
    session['url'] = {}
    session['tracks'] = {}
    session['tracks']['seeds'] = []
    session['tracks']['hold'] = []
    session['tracks']['hold'] = []
    session['url']['popularity'] = 40
    session['url']['length'] = 20


"""
INPUT: SEED ARTIST ID + SEED TRACK IDS AND POPULARITY FROM SESSION
OUTPUT: SEARCH URL
"""
def generate_url(id):
    #limit = int(session['features']['length']) + 10

    url = f"https://api.spotify.com/v1/recommendations?limit=30&market=US&max-popularity={session['url']['popularity']}&seed_artists={id}"
    
    seeds = session['tracks']['seeds']

    if len(seeds) == 0:
        return url
    elif len(seeds) == 1:
        url += '&seed_tracks='
        url += seeds[0]
    else:
        url += '&seed_tracks='
        seeds = "%2C".join(seeds)
        url += seeds
    
    return url
    


"""
INPUT: ARTIST NAME TO QUERY
OUTPUT: TOP THREE RESULTS FROM SPOTIFY IN FORMAT (NAME, ID)
"""
def search_artist(input):
    
    query = input.replace(' ','%20')
    url = f"https://api.spotify.com/v1/search?q={query}&type=artist&market=US&limit=3"
    headers = {
            'Authorization': 'Bearer ' + session['access_token'],
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'SameSite': 'None'
        }
    response = requests.get(url, headers=headers)
    response_json = response.json()
    if response.status_code not in range(200,299):
        print(response.status_code, response.content)
        return None

    
    top_three = [(artist['name'], artist['id']) for artist in response_json['artists']['items']]
    
    return top_three





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
    output['id'] = track['id']

    return output

"""
INPUT: URL FOR FETCHING RECCOMENDATION FROM SPOTIFY API
OUTPUT: DICTIONARY OF TRACKS WITH FORMAT "URL: TRACK DICT"
"""
def get_tracks():
    url = generate_url(session['url']['artist_id'])
    print(url)
    session['url']['previous'] = url
    

    headers = {
            'Authorization': 'Bearer ' + session['access_token'],
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code not in range(200,299):
        print(response.status_code, response.content)
        return None

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
    
    if public == "public":
        public = True
    else:
        public = False

    headers = {
            'Authorization': 'Bearer ' + session['access_token'],
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    body = {
        "name": f"{name}",
        "description": f"{description}",
        "public": f"{public}"
    }
    response = requests.post(url, headers=headers, data=json.dumps(body))
    
    return response
    

def populate_playlist(playlist_id):
    
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {
            'Authorization': 'Bearer ' + session['access_token'],
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    body = {
        "uris": list(session['tracks']['current'].keys())
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(body))

    return response
    
