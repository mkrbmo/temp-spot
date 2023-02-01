import pytest
from application import create_app
from flask import session

@pytest.fixture()
def app():
    app = create_app()
    app.config.from_pyfile('config.py')
    app.config.update({
        "TESTING": True,
    })
    

    # other setup can go here

    yield app

    # clean up / reset resources here

@pytest.fixture()
def client(app):
    with app.test_client() as testing_client:
        with app.app_context():

            yield testing_client



