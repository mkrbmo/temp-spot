from flask import Blueprint, render_template, request, session, redirect, url_for
import requests, json
from application import pipe
from application.functions import generate_reccomendation_url, check_token, clean_track

bp = Blueprint('routes', __name__)

@bp.route('/')
def home():
    if 'access_token' in session:
        return redirect(url_for('routes.analysis'))
    return redirect(url_for('authorize.authorize'))

@bp.route('/test')
def test():
    return render_template('test.html')

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
        
        limit = 30

        url = generate_reccomendation_url(emotion, limit)
        
        headers = {
            'Authorization': 'Bearer ' + session['access_token'],
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        response = requests.get(url, headers=headers)
        
        #seeds = response.json()['seeds']
        response_tracks = response.json()['tracks']
        
        
        tracks = [clean_track(track) for track in response_tracks]

        sent_tracks = tracks[0:10]
        queued_tracks = tracks[10:]
        
        
        
        

        return render_template('results.html', tracks=sent_tracks, sentence=input, queue=queued_tracks)

    return render_template('search.html')

"""
@bp.route('/fetch_tracks')
def fetch_tracks(url):

    token = check_token(session)
    if token:
        session['previous_url'] = request.path
        return token
    url = session['saved_url']
    headers = {
            'Authorization': 'Bearer ' + session['access_token'],
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    response = requests.get(url, headers=headers)
    response_tracks = response.json()['tracks']
    tracks = [clean_track(track) for track in response_tracks]
    return tracks
"""




    
