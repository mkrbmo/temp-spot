import os
from flask import Flask
from transformers import pipeline

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True) 
    app.config.from_pyfile('config.py')

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import authorize, routes
    app.register_blueprint(authorize.bp)
    app.register_blueprint(routes.bp)

    pipe = pipeline('sentiment-analysis', model="arpanghoshal/EmoRoBERTa", top_k=None)

    return app