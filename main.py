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

@app.route('/stories', methods=['GET'])
def stories():
    cursor, stories = data.stories(
        int(flask.request.args.get('cursor', 0)),
        int(flask.request.args.get('limit', 10))
    )
    return flask.jsonify(_build_response(cursor, stories, 'stories'))

@app.route('/stories/<string:id>', methods=['GET'])
def story_by_id(id):
    return flask.jsonify(
        _build_response(None, data.story_by_id(id), 'stories')
    )

@app.route('/meta/<string:story_id>', methods=['GET'])
def stories_metadata(story_id):
    cursor, stories = data.metadata_by_story_id(
        story_id,
        int(flask.request.args.get('cursor', 0)),
        int(flask.request.args.get('limit', 10))
    )
    return flask.jsonify(_build_response(cursor, stories, 'meta'))

@app.route('/stories/meta_search', methods=['GET'])
def search_meta():
    cursor, stories = data.search_meta(
        flask.request.args,
        int(flask.request.args.get('cursor', 0)),
        int(flask.request.args.get('limit', 10))
    )

    return flask.jsonify(_build_response(cursor, stories, 'stories'))

@app.route('/stories/text_search', methods=['GET'])
def search():
    cursor, stories = data.search_text(
        flask.request.args,
        int(flask.request.args.get('cursor', 0)),
        int(flask.request.args.get('limit', 10))
    )
    
    return flask.jsonify(_build_response(cursor, stories, 'stories'))