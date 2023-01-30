from flask import Blueprint, render_template, request, session
import requests, json
from application import pipe
from functions import generate_reccomendation_url, format_reccomendation_data, transform_to_audio_features

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
        
        response = requests.get(base_url+input, headers=headers)

        jsonData = response.text
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
def reccomendation():
    if request.method == "POST":
        parameters = format_reccomendation_data(request.form.to_dict())
        url = generate_reccomendation_url(parameters)

        headers = {
            'Authorization': 'Bearer ' + session['access_token'],
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        print(url)
        response = requests.get(url, headers=headers)
        data = response.json()

        return render_template('reccomendation.html', response=data)

    return render_template('reccomendation.html')








    
