import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from . import config
#from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('authorize', __name__, url_prefix='/authorize')

@bp.route('/', methods=('GET', 'POST'))
def authorize():
    if request.method == 'POST':
        clientId = config.clientId
        secret = config.secret
        redirectURI = config.redirectURI
        scopes = config.scopes

        url = 'https://accounts.spotify.com/en/authorize?'
        parameters = 'response_type=code&client_id=' + clientId + '&redirect_uri=' + redirectURI + '&scope=' + scopes + '&state=' + state_key

        response = url

    return render_template('authorize/login.html')
