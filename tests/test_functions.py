
from application.functions import generate_reccomendation_url, format_reccomendation_data, generate_key, transform_emotion_to_features
from flask import current_app as app




def test_generateKey():
    assert len(generate_key(5))== 5

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

