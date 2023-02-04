import requests, base64, time 
from application.functions import generate_key
from flask import (
    Blueprint, redirect, render_template, request, session, make_response
)
from flask import current_app as app

bp = Blueprint('authorize', __name__)


#INITIATION VIEW FOR AUTHORIZING SPOTIFY CONNECTION
@bp.route('/authorize/', methods=('GET', 'POST'))
def authorize():
    
    if request.method == 'POST':
        clientId = app.config['SPOTIFY_CLIENT_ID']
        redirectURI = app.config['SPOTIFY_REDIRECT_URI']
        scopes = app.config['SPOTIFY_SCOPES']
        stateKey = generate_key(16)
        session['key'] = stateKey

        url = 'https://accounts.spotify.com/en/authorize?'
        parameters = 'response_type=code&client_id=' + clientId + '&redirect_uri=' + redirectURI + '&scope=' + scopes + '&state=' + stateKey

        response = make_response(redirect(url + parameters))
        
        return response

        

    return render_template('login.html')

#CALLBACK VIEW FOR REQUESTING TOKEN
@bp.route('/callback/')
def callback():
    state = request.args.get('state')
    if state != session['key'] or state == None :
        return render_template('login.html', errorMsg = "state mismatch") #ADD ERROR MESSAGE HANDLING IN TEMPLATE
    elif request.args.get('error'):
        return render_template('login.html', errorMsg = "spotify error")
    
    code = request.args.get('code')
    authString = app.config['SPOTIFY_CLIENT_ID']+':'+ app.config['SPOTIFY_SECRET']
    b64AuthString = base64.urlsafe_b64encode(authString.encode()).decode()

    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': "Basic " + b64AuthString, 
        'Accept': 'application/json', 
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    body = {
        'code': code, 
        'redirect_uri': app.config['SPOTIFY_REDIRECT_URI'], 
        'grant_type': 'authorization_code',
    }
    
    response = requests.post(url, headers=headers, data=body)
    
    #TOKEN RESPONSE
    if response.status_code != 200:
        return redirect('/', error='invalid token')

    payload = response.json()
    session['access_token'] = payload['access_token']
    session['refresh_token'] = payload['refresh_token']
    session['expiration'] = time.time() + payload['expires_in']

    print('post token:', session)
    
    return redirect('/analysis')#CHANGE TO PREVIOUS URL

