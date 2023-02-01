
from application.functions import generate_reccomendation_url, format_reccomendation_data, generate_key, transform_emotion_to_features
from application.authorize import check_token, refresh_token
from tests.conftest import client
from flask import session


def test_generateKey():
    assert len(generate_key(5)) == 5

def test_formatReccomendationData():
    input = {'energy': 'low', 'valence': 'low', 'tempo': 'low', 'seed': 'electro', 'response': ''}
    expected_output = {'energy': {'min': 0.0, 'max': 0.35}, 'valence': {'min': 0.0, 'max': 0.35}, 'tempo': {'min': 0.0, 'max': 0.35}, 'seed': 'electro'}
    assert format_reccomendation_data(input) == expected_output

def test_generateReccomendationURL():
    input = {'energy': 'low', 'valence': 'mid', 'genre': ['electro', ' industrial', ' trance']}
    expected_result = "https://api.spotify.com/v1/recommendations?limit=5&market=US&seed_genres=electro%2Cindustrial%2Ctrance&min_energy=0.0&max_energy=0.35&min_valence=0.35&max_valence=0.65"
    assert generate_reccomendation_url(input) == expected_result


def test_transform_emotion_to_features():
    assert transform_emotion_to_features('admiration') == {'energy': 'mid', 'valence': 'high', 'genre': ['alternative', ' happy', ' indie', ' pop']}
    assert transform_emotion_to_features('neutral') == {'energy': 'mid', 'valence': 'mid', 'genre': ['world-music', ' chill']}


def test_check_token(client):
    with client.session_transaction() as session:
        session['access_token'] = 'BQBsZrrLI2MVEFkwYMwZpljqUF4-W-_CU-hPzjohkWwwXOR5w7Lwl_xWmrIxS2mxjjaFQZkE0agMOsxRY2Qeafi1voTw4DSFq9Qg88g-Py1hc296ljWnWGHBT7wgEUM-gbdxtsbsbH7QAKS4Ns640KLXsyRTZQqla7Lp3MnL-sPyjtV69bPASPZazpxvndqHVN0CCGrAhJpf2k6Hrw'
        session['refresh_token'] = 'AQAN7JZvPiWpfIpcL3Bwe6yBgys4kH8YkDVUnBPYAwQDCdSViJl0mHnftlrxPhJvEqoYgsDcnxHOISQ3Xu2wPCnnG9KKdkohUy6mfDnx_T6TGfzWNXQ7cISwIcZRHSPuJkg'
        session['expiration'] = 1000000000000.0
    
        assert check_token(session) == None
        assert session['expiration'] == 1000000000000.0
        assert session['access_token'] == 'BQBsZrrLI2MVEFkwYMwZpljqUF4-W-_CU-hPzjohkWwwXOR5w7Lwl_xWmrIxS2mxjjaFQZkE0agMOsxRY2Qeafi1voTw4DSFq9Qg88g-Py1hc296ljWnWGHBT7wgEUM-gbdxtsbsbH7QAKS4Ns640KLXsyRTZQqla7Lp3MnL-sPyjtV69bPASPZazpxvndqHVN0CCGrAhJpf2k6Hrw'
"""
    #with client.session_transaction() as session:
        session['expiration'] = 1000.0
        check_token(session)
        assert session['expiration'] != 1000.0

def test_refresh_token(client):
    token = 'failure'
    assert refresh_token(token) == None
    token = 'AQAN7JZvPiWpfIpcL3Bwe6yBgys4kH8YkDVUnBPYAwQDCdSViJl0mHnftlrxPhJvEqoYgsDcnxHOISQ3Xu2wPCnnG9KKdkohUy6mfDnx_T6TGfzWNXQ7cISwIcZRHSPuJkg'
    assert len(refresh_token(token)) == 2
"""
    