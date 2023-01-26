from flask import Blueprint, render_template, request, session
import requests, json
from . import pipe

bp = Blueprint('spotif', __name__)

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

        labels = pipe(input)[0]
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
        parameters = {}
    
        for item in request.form:
            if item != 'response':
                parameters[item] = request.form[item]
        
        getReccomendations(parameters)

    return render_template('req.html')

def getReccomendations(parameters):
    print(parameters)
    for param in parameters:
        match param:
            case 'low':
                param['min'] = 0.0
                param['max'] = 0.5
            case 'mid':
                param['min'] = 0.35
                param['max'] = 0.65
            case 'high':
                param['min'] = 0.65
                param['max'] = 1.0

        print(param)




    
