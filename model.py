import flask_pymongo as pymongo
from . import config

def model():
    if config.model() == 'mongodb':
        return MongoDB()
    raise ValueError('Unsupported data model: ', config.model())

class MongoDB:

    mongo = None

    @classmethod
    def init_app(cls, app):
        cls.mongo = pymongo.PyMongo(app)
        cls.mongo.init_app(app)
    
    @classmethod
    def news_metadata(cls, story_id, cursor=0, limit=10):
        return list(
            cls.mongo.db.Structured.find(
                {'rp_story_id': story_id},
                {'_id': 0}
            ).skip(cursor).limit(limit)
        )

    @classmethod
    def news(cls, cursor=0, limit=10):
        return list(
            cls.mongo.db.Unstructured.find(
                {},
                {'_id': 0}
            ).skip(cursor).limit(limit)
        )
    