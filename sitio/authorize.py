import random, string, requests, base64, time

from flask import (
    Blueprint, redirect, render_template, request, session, make_response
)
from . import config

bp = Blueprint('authorize', __name__)

#GENERATOR FUNCTION FOR STATE KEY
def generateKey(length):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))

#INITIATION VIEW FOR AUTHORIZING SPOTIFY CONNECTION
@bp.route('/authorize/', methods=('GET', 'POST'))
def authorize():
    if request.method == 'POST':
        clientId = config.clientId
        redirectURI = config.redirectURI
        scopes = config.scopes
        stateKey = generateKey(16)
        session['key'] = stateKey

        url = 'https://accounts.spotify.com/en/authorize?'
        parameters = 'response_type=code&client_id=' + clientId + '&redirect_uri=' + redirectURI + '&scope=' + scopes + '&state=' + stateKey

        response = make_response(redirect(url + parameters))

        return response

        

    return render_template('authorize/login.html')

#CALLBACK VIEW FOR REQUESTING TOKEN
@bp.route('/callback/')
def callback():
    state = request.args.get('state')
    if state != session['key'] or state == None :
        return render_template('authorize/login.html', errorMsg = "state mismatch") #ADD ERROR MESSAGE HANDLING IN TEMPLATE
    elif request.args.get('error'):
        return render_template('authorize/login.html', errorMsg = "spotify error")
    
    code = request.args.get('code')
    authString = config.clientId+':'+config.secret
    b64AuthString = base64.urlsafe_b64encode(authString.encode()).decode()

    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': "Basic " + b64AuthString, 
        'Accept': 'application/json', 
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    body = {
        'code': code, 
        'redirect_uri': config.redirectURI, 
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

    print(session)
    
    return redirect('/fetch')

''' RESPONSE TOKEN EXAMPLE
{'access_token': 'BQAnWIPnU4L0D7iiVziJjHWbn5WnpAARSSugDWfX8juoPloSqz-u20Pi7-GVGGk0bV6ESx1FYDnsN8R-C6NkDxobzuteCMcLbJU_83Lwb1A6lri1Mkxb09WLJPVD8QELvMWPfVcdOd0-Fvj11XKq3f4fzOE2Ad3g67IakNtTJJs5kmZHqlOHddhjkJ-T9sQavlEM6X-Mtig', 
'token_type': 'Bearer', 
'expires_in': 3600, 
'refresh_token': 'AQC3rmT_h6bJ10XuiNfZWTucmSHDu953g7-LW9sxOGlEoyIrYgryVxSwjKgadWFTQIGS_4T_iOY7ozgEvJ9ftcoyLFxgemOgtHbCU0IAtWJuIwHXwAnGCKMcQ4MkWcp4R-Y', 
'scope': 'user-read-recently-played'}
'''

def refreshToken():
    #code = request.args.get('code')
    authString = config.clientId+':'+config.secret
    b64AuthString = base64.urlsafe_b64encode(authString.encode()).decode()

    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': "Basic " + b64AuthString, 
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    body = {
        'refresh_token': session['refresh_token'],
        'grant_type': 'authorization_code',
    }
    response = requests.post(url, headers=headers, data=body)

    if response.status_code != 200:
        return redirect('/', error='invalid token')

    payload = response.json()
    session['access_token'] = payload['access_token']
    session['refresh_token'] = payload['refresh_token']
    session['expiration'] = time.time() + payload['expires_in']