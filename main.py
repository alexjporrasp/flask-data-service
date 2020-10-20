import flask
from . import config
from . import model

app = flask.Flask(__name__)
app.config['MONGO_URI'] = config.mongo_uri()
data = model.model()
data.init_app(app)

def _build_response(cursor, result, collection):
    return {
        'data': result,
        'collection': collection,
        'next': cursor
    }

@app.route('/stories/', methods=['GET'])
def stories():
    cursor, stories = data.stories(
        int(flask.request.args.get('cursor', 0)),
        int(flask.request.args.get('limit', 10))
    )
    return flask.jsonify(_build_response(cursor, stories, 'stories'))

@app.route('/stories/meta/<string:story_id>', methods=['GET'])
def stories_metadata(story_id):
    cursor, stories = data.stories_metadata(
        story_id,
        int(flask.request.args.get('cursor', 0)),
        int(flask.request.args.get('limit', 10))
    )
    return flask.jsonify(_build_response(cursor, stories, 'meta'))



@app.route('/stories/search/', methods=['GET'])
def search():
    cursor, stories = data.search(
        flask.request.args,
        int(flask.request.args.get('cursor', 0)),
        int(flask.request.args.get('limit', 10))
    )
    
    return flask.jsonify(_build_response(cursor, stories, 'stories'))