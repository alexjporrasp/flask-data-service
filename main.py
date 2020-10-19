import flask
from . import config
from . import model

app = flask.Flask(__name__)
app.config['MONGO_URI'] = config.mongo_uri()
data = model.model()
data.init_app(app)

@app.route('/meta/<string:story_id>', methods=['GET'])
def stories_metadata(story_id):
    return flask.jsonify(data.news_metadata(story_id))

@app.route('/news', methods=['GET'])
def stories():
    return flask.jsonify(data.news())