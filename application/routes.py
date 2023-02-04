from flask import Blueprint, render_template, request, session, redirect, url_for
import requests, json
from application import pipe
from application.functions import generate_reccomendation_url, format_reccomendation_data, check_token

bp = Blueprint('routes', __name__)

@bp.route('/')
def home():
    if 'access_token' in session:
        return redirect(url_for('routes.analysis'))
    return redirect(url_for('authorize.authorize'))

"""
GENERAL FORM FOR FETCHING DATA FROM SPOTIFY API FOR DEVELOPMENT PURPOSES
REMOVE FROM PRODUCTION SITE
"""
@bp.route('/fetch', methods=('GET', 'POST'))
def fetch():
    if request.method == 'POST':
        input = request.form['inputURL']

        base_url = 'https://api.spotify.com/v1/'
        headers = {
            'Authorization': 'Bearer ' + session['access_token']
        }
        
        response = requests.get(base_url+input, headers=headers)

        jsonData = response.text
        jsonData = json.dumps(response.json(), indent=2)

        return render_template('fetch.html', response=jsonData)

    return render_template('fetch.html')

""" 
INPUT: user supplied string from form
TRANSFORMATION: string - emotion - audio features - song reccomendation list
RETURNS: list of reccomended song
"""
@bp.route('/analysis', methods=('GET', 'POST'))
def analysis():


    if request.method == 'POST':
        
        token = check_token(session)
        if token:
            session['previous_url'] = request.path
            return token


        input = request.form['input-sentence']

        emotion = pipe(input)[0][0]['label']
        
        url = generate_reccomendation_url(emotion)
        print(url)
        headers = {
            'Authorization': 'Bearer ' + session['access_token'],
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        response = requests.get(url, headers=headers)
        print(response.json())
        #seeds = response.json()['seeds']
        tracks = response.json()['tracks']
        
        
        


        return render_template('results.html', tracks=tracks, sentence=input)

    return render_template('search.html')






    
