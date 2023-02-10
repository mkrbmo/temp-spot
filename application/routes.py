from flask import (
    Blueprint, 
    render_template, 
    request, session, 
    redirect, url_for, 
    jsonify
)
import requests, json, random
from application import pipe
from application.functions import (
    generate_reccomendation_url, 
    check_token, 
    get_tracks, get_user, 
    create_playlist, 
    populate_playlist
)

bp = Blueprint('routes', __name__)

@bp.route('/')
def home():
    if check_token(session) != None:
        return redirect(url_for('authorize.authorize'))
    return redirect(url_for('routes.analysis'))
    

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
        limit = 15
        
        token = check_token(session)
        if token:
            session['previous_url'] = request.path
            return token

        input = request.form['input-sentence']
        emotion = pipe(input)[0][0]['label']
        
        url = generate_reccomendation_url(emotion, limit)
        session['current_fetch_url'] = url

        tracks = get_tracks(url)

        #arbitrary separation of first 10 tracks by URI
        keys = [_ for _ in tracks.keys()]
        current = keys[:10]
        queued = keys[10:15]

        session['all_tracks'] = keys
        session['current_tracks'] = {k:tracks[k] for k in current}
        session['queued_tracks'] = {k:tracks[k] for k in queued}
        session['queued_keys'] = queued

        return render_template('results.html', sentence=input)

    return render_template('search.html')


@bp.route('/swap_track/<uri>')
def swap_track(uri):
    try:
        session['current_tracks'].pop(uri)
    except KeyError:
        pass #add funcitonality
    key = session['queued_keys'].pop()
    new_track = {key: session['queued_tracks'].pop(key, None)}
    session['current_tracks'].update(new_track)
    
    if len(session['queued_tracks']) < 3:
        tracks = get_tracks(session['current_fetch_url'])
        
        for uri, track in tracks.items():
            if uri not in session['all_tracks']:
                session['queued_keys'].append(uri)
                session['queued_tracks'].update({uri:track})

    return jsonify(new_track)

@bp.route('/send_playlist/<name>/<public>/<description>')
def send_playlist(name, public, description):

    user_response = get_user()
    if user_response.status_code != 200:
        return {"error": "Invalid User ID"}
    
    user_id = user_response.json()['id']
    playlist_response = create_playlist(user_id, name, description, public)
    
    
    if playlist_response.status_code != 201:
        return {"error": "Playlist Creation Error"}

    playlist_id = playlist_response.json()['id']

    population_response = populate_playlist(playlist_id)
    if population_response.status_code != 201:
        return {"error": "Playlist Population Error"}

    return 'OK'
    
