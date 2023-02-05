
from application.functions import generate_reccomendation_url, generate_key, clean_track, check_token, refresh_token
from tests.conftest import client
from flask import session


def test_generateKey():
    assert len(generate_key(5)) == 5

def test_generateReccomendationURL():
    expected_result = "https://api.spotify.com/v1/recommendations?limit=5&market=US&seed_genres=alternative%2Chappy%2Cindie%2Cpop&min_energy=0.35&max_energy=0.65&min_valence=0.65&max_valence=1.0"
    assert generate_reccomendation_url('admiration') == expected_result


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
    
def test_clean_track():
    false = False
    true = True
    input = {
        "album": {
            "album_type": "SINGLE",
            "artists": [
            {
                "external_urls": {
                "spotify": "https://open.spotify.com/artist/2txHhyCwHjUEpJjWrEyqyX"
                },
                "href": "https://api.spotify.com/v1/artists/2txHhyCwHjUEpJjWrEyqyX",
                "id": "2txHhyCwHjUEpJjWrEyqyX",
                "name": "Tom Odell",
                "type": "artist",
                "uri": "spotify:artist:2txHhyCwHjUEpJjWrEyqyX"
            }
            ],
            "external_urls": {
            "spotify": "https://open.spotify.com/album/3Bi2XO3N9AL5f7VvVmyVna"
            },
            "href": "https://api.spotify.com/v1/albums/3Bi2XO3N9AL5f7VvVmyVna",
            "id": "3Bi2XO3N9AL5f7VvVmyVna",
            "images": [
            {
                "height": 640,
                "url": "https://i.scdn.co/image/ab67616d0000b2733aeff37d3f480564f6e88059",
                "width": 640
            },
            {
                "height": 300,
                "url": "https://i.scdn.co/image/ab67616d00001e023aeff37d3f480564f6e88059",
                "width": 300
            },
            {
                "height": 64,
                "url": "https://i.scdn.co/image/ab67616d000048513aeff37d3f480564f6e88059",
                "width": 64
            }
            ],
            "name": "Another Love (Zwette Edit)",
            "release_date": "2013-09-27",
            "release_date_precision": "day",
            "total_tracks": 1,
            "type": "album",
            "uri": "spotify:album:3Bi2XO3N9AL5f7VvVmyVna"
        },
        "artists": [
            {
            "external_urls": {
                "spotify": "https://open.spotify.com/artist/2txHhyCwHjUEpJjWrEyqyX"
            },
            "href": "https://api.spotify.com/v1/artists/2txHhyCwHjUEpJjWrEyqyX",
            "id": "2txHhyCwHjUEpJjWrEyqyX",
            "name": "Tom Odell",
            "type": "artist",
            "uri": "spotify:artist:2txHhyCwHjUEpJjWrEyqyX"
            },
            {
            "external_urls": {
                "spotify": "https://open.spotify.com/artist/6J2749jPHYhAZUq79rsNi0"
            },
            "href": "https://api.spotify.com/v1/artists/6J2749jPHYhAZUq79rsNi0",
            "id": "6J2749jPHYhAZUq79rsNi0",
            "name": "Zwette",
            "type": "artist",
            "uri": "spotify:artist:6J2749jPHYhAZUq79rsNi0"
            }
        ],
        "disc_number": 1,
        "duration_ms": 394573,
        "explicit": false,
        "external_ids": {
            "isrc": "GBARL1301232"
        },
        "external_urls": {
            "spotify": "https://open.spotify.com/track/5snyhxAh55A2wlNRH7VVZJ"
        },
        "href": "https://api.spotify.com/v1/tracks/5snyhxAh55A2wlNRH7VVZJ",
        "id": "5snyhxAh55A2wlNRH7VVZJ",
        "is_local": false,
        "is_playable": true,
        "name": "Another Love - Zwette Edit",
        "popularity": 63,
        "preview_url": "https://p.scdn.co/mp3-preview/d6a97d0a24f987bf474983a0a7635b457fc88b8a?cid=60e8f2f1ff2e46ea88a8b34c45b3183e",
        "track_number": 1,
        "type": "track",
        "uri": "spotify:track:5snyhxAh55A2wlNRH7VVZJ"
        }

    output = {'album': "Another Love (Zwette Edit)", 'artists': 'Tom Odell, Zwette', 'title':"Another Love - Zwette Edit", 'cover_url':"https://i.scdn.co/image/ab67616d000048513aeff37d3f480564f6e88059", 'preview_url': "https://p.scdn.co/mp3-preview/d6a97d0a24f987bf474983a0a7635b457fc88b8a?cid=60e8f2f1ff2e46ea88a8b34c45b3183e"}
    assert clean_track(input) == output