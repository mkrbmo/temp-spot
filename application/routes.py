from flask import Blueprint, render_template, request, session
import requests, json

from flask import current_app as app

bp = Blueprint('routes', __name__)

@bp.route('/')
def home():
    return render_template('base.html', error=None)

@bp.route('/fetch', methods=('GET', 'POST'))
def fetch():
    if request.method == 'POST':
        input = request.form['inputURL']

        base_url = 'https://api.spotify.com/v1/'
        headers = {
            'Authorization': 'Bearer ' + session['access_token']
        }
        print(base_url+input)
        response = requests.get(base_url+input, headers=headers)

        jsonData = response.json()
        jsonData = json.dumps(response.json(), indent=2)

        return render_template('fetch.html', response=jsonData)

    return render_template('fetch.html')

@bp.route('/analysis', methods=('GET', 'POST'))
def analysis():
    if request.method == 'POST':
        input = request.form['inputSentence']

        labels = app.pipe(input)[0]
        emotions = []

        for each in labels:
            each['score'] = round(each['score'], 3)
            if each['score'] >= 0.01:
                emotions.append(each)
                

        return render_template('analysis.html', response=emotions)

    return render_template('analysis.html')

@bp.route('/req', methods=('GET', 'POST'))
def req():
    if request.method == "POST":
        #parameters = formatReccomendationFormData(request.form)
        #url = generateReccomendationURL(parameters)
        print(request.form)
    return render_template('req.html')


def formatReccomendationData(form):
    parameters = {}
    del form['response']

    for item in form:
            if form[item] == 'low':
                parameters[item] = {'min': 0.0, 'max': 0.35}
            if form[item] == 'mid':
                parameters[item] = {'min': 0.35, 'max': 0.65}
            if form[item] == 'high':
                parameters[item] = {'min': 0.65, 'max': 1.0}

    return parameters


def generateReccomendationURL(parameters):
    limit = 5
    url = f"https://api.spotify.com/v1/recommendations?limit={limit}&market=EN&seed_genres={parameters['seed']}&min_energy={parameters['energy']['min']}&max_energy={parameters['energy']['max']}&min_tempo={parameters['tempo']['min']}&max_tempo={parameters['tempo']['max']}&min_valence={parameters['valence']['min']}&max_valence={parameters['valence']['max']}"
    
    return url





    
