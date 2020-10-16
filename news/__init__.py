import flask

def create_app(config, debug=False, testing=False, config_overrides=None):
    app = flask.Flask(__name__)
    app.config.from_object(config)
    app.debug = debug
    app.testing = testing

    if config_overrides:
        app.config.update(config_overrides)