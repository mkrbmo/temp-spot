from flask import (
    Blueprint, 
    render_template, 
    request, session, 
    redirect, url_for, 
    jsonify
)
import requests, json, random

from application.functions import (
    check_token, 
    get_tracks, get_user, 
    create_playlist, 
    populate_playlist,
    populate_tracks
)

bp = Blueprint('routes', __name__)

@bp.route('/')
def home():
    session.clear()
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
        
        if not session.get('features'):
            session['features'] = {}
            session['features']['target_popularity'] = 40
            session['features']['length'] = 20

        if check_token(session) != None:
            return redirect(url_for('authorize.authorize'))
        
        sentence = request.form['input-sentence']
        
        populate_tracks(sentence)
        
        return render_template('results.html', sentence=sentence)

    return render_template('search.html')


@bp.route('/delete_track/<uri>')
def delete_track(uri):
    try:
        session['current_tracks'].pop(uri)
        return "OK"
    except KeyError:
        pass #add funcitonality

@bp.route('/add_track')
def add_track():

    key = session['queued_keys'].pop()
    new_track = session['queued_tracks'].pop(key, None)
    session['current_tracks'].update(new_track)
    
    if len(session['queued_tracks']) < 3:
        if check_token(session) != None:
            return redirect(url_for('authorize.authorize'))
        #ADD REROUTING FOR PREVIOUS URL
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
    print(population_response.text)
    if population_response.status_code != 201:
        return {"error": "Playlist Population Error"}

    return 'OK'
    
@bp.route('/update_options', methods=('GET', 'POST'))
def update_options():
    responses = request.get_json()
    session['features']['target_popularity'] = responses['popularity']
    session['features']['target_instrumentalness'] = responses['instrumentalness']
    session['features']['length'] = int(responses['length'])
    
    if check_token(session) != None:
            return redirect(url_for('authorize.authorize'))
        
    tracks = populate_tracks(responses['prompt'])
    print(tracks)
    return jsonify(tracks)
    
    
