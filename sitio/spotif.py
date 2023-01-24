from flask import Blueprint, render_template, request, session
import requests, json

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