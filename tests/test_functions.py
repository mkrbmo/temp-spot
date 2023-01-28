from application.authorize import generateKey
from application.routes import generateReccomendationURL
from flask import current_app as app



def test_generateKey():
    assert len(generateKey(5))== 5


def test_generateReccomendationURL():
    parameters = {'energy': {'min': 0.4, 'max': 0.6}, 'valence': {'min': 0.4, 'max': 0.6}, 'tempo': {'min': 0.4, 'max': 0.6}, 'seed': 'electro'}
    expected_result = "https://api.spotify.com/v1/recommendations?limit=5&market=EN&seed_genres=electro&min_energy=0.4&max_energy=0.6&min_tempo=0.4&max_tempo=0.6&min_valence=0.4&max_valence=0.6"
    assert generateReccomendationURL(parameters) == expected_result

