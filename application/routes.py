from flask import (
    Blueprint, 
    render_template, 
    request, session, 
    redirect, url_for, 
    jsonify
)

from application.functions import (
    check_token, 
    get_tracks, get_user, 
    create_playlist, 
    populate_playlist,
    
    search_artist,
    initialize_session,

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


@bp.route('/suggest/',  methods=('GET', 'POST'))
def suggest():
    artist = request.args.get('q')

    if check_token(session) != None:
            return redirect(url_for('authorize.authorize'))
        
    suggestions = search_artist(artist)

    if suggestions == None:
        return ('', 204)

    return suggestions



""" 
INPUT: user supplied string from form
TRANSFORMATION: string - emotion - audio features - song reccomendation list
RETURNS: list of reccomended song
"""
@bp.route('/analysis', methods=('GET', 'POST'))
def analysis():
    if check_token(session) != None:
            return redirect(url_for('authorize.authorize'))
        
    if request.method == 'POST':
        
        if not session.get('url'):
            initialize_session()
        
        seed_artist = request.form['search-artist']

        three = search_artist(seed_artist)
        artist_id = three[0][1]
        session['url']['artist_id'] = artist_id
        session['url']['artist_name'] = three[0][0]
        
        tracks = get_tracks()
        if tracks == None:
            return render_template('search.html', error='something went wrong')

        track_uris = [_ for _ in tracks.keys()]
        current_uris = track_uris[:session['url']['length']]
        queued_uris = track_uris[session['url']['length']:]

        session['tracks']['seeds'] = []
        session['tracks']['hold'] = []

        session['tracks']['omit'] = current_uris
        session['tracks']['current'] = {k:tracks[k] for k in current_uris}
        session['tracks']['queue'] = [tracks[k] for k in queued_uris]
        
        return render_template('results.html')

    return render_template('search.html')


@bp.route('/delete_track/<uri>')
def delete_track(uri):
    try:
        session['tracks']['current'].pop(uri)
        return "OK"
    except KeyError:
        pass #add funcitonality


@bp.route('/add_track')
def add_track():

    new_track = session['tracks']['queue'].pop()
    session['tracks']['current'].update({new_track['uri']:new_track})
    
    if len(session['tracks']['queue']) < 3:
        if check_token(session) != None:
            return redirect(url_for('authorize.authorize'))
        #ADD REROUTING FOR PREVIOUS URL
        tracks = get_tracks()
        
        if tracks != None:
            for uri, track in tracks.items():
                if uri not in session['tracks']['omit']:
                    session['tracks']['queue'].append(track)
    return jsonify(new_track)

@bp.route('/update_options', methods=('GET', 'POST'))
def update_options():
    responses = request.get_json()
    session['url']['popularity'] = responses['popularity']
    session['url']['length'] = int(responses['length'])
    
    if check_token(session) != None:
            return redirect(url_for('authorize.authorize'))
        
    tracks = get_tracks()
    if tracks == None:
        return "405" ##WUT

    track_uris = [_ for _ in tracks.keys()]
    current_uris = track_uris[:session['url']['length']]
    queued_uris = track_uris[session['url']['length']:]

    session['tracks']['omit'] = current_uris
    session['tracks']['current'] = {k:tracks[k] for k in current_uris}
    session['tracks']['queue'] = [tracks[k] for k in queued_uris]


    return jsonify(session['tracks']['current'])

    


@bp.route('/send_playlist',methods=('GET', 'POST'))
def send_playlist():
    responses = request.get_json()
    name = responses['name']
    description = responses['description']
    public = responses['public']

    user_response = get_user()
    if user_response.status_code not in range(200,299):
        return {"error": "Invalid User ID"}
    user_id = user_response.json()['id']
    

    playlist_response = create_playlist(user_id, name, description, public)
    if playlist_response.status_code not in range(200,299):
        return {"error": "Playlist Creation Error"}
    playlist_id = playlist_response.json()['id']
    

    population_response = populate_playlist(playlist_id)
    
    if population_response.status_code != 201:
        return {"error": "Playlist Population Error"}

    return 'OK'


@bp.route('/mixin_track/<id>/<uri>', methods=('GET', 'POST'))
def mixin_track(id, uri):
    if len(session['tracks']['seeds']) >= 4:
        session['tracks']['seeds'].pop(0)

    session['tracks']['seeds'].append(id)
    
    session['tracks']['hold'].append({uri:session['tracks']['current'][uri]})
    

    if check_token(session) != None:
            return redirect(url_for('authorize.authorize'))
    
    tracks = get_tracks()
    if tracks == None:
        return "405" ##WUT

    track_uris = [_ for _ in tracks.keys()]
    current_uris = track_uris[:session['url']['length']-len(session['tracks']['hold'])]
    queued_uris = track_uris[session['url']['length']-len(session['tracks']['hold']):]

    session['tracks']['omit'] = current_uris
    session['tracks']['current'] = {k:tracks[k] for k in current_uris}
    for track in session['tracks']['hold']:
        session['tracks']['current'].update(track)
    
    session['tracks']['queue'] = [tracks[k] for k in queued_uris]


    return jsonify(session['tracks']['current'])
