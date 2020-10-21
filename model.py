import flask_pymongo as pymongo
import re
import config

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
    def stories(cls, cursor=0, limit=10):
        """
        Select all stories.
        """
        stories = list(
            cls.mongo.db.Unstructured.find(
                {},
                {'_id': 0}
            ).skip(cursor).limit(limit)
        )

        next_cursor = cursor + limit if len(stories) == limit else None

        return next_cursor, stories

    @classmethod
    def story_by_id(cls, story_id=''):
        """
        Return the story with the given <story_id>.
        """
        return list(cls.mongo.db.Unstructured.find(
            { 'rp_story_id': story_id },
            { '_id': 0 }
        ))

    @classmethod
    def _numeric_modifier(cls, param: str):
        match = re.match(r'(<|>|(<=)|(>=)|(==))((0|[1-9][0-9]*)(\.[0-9]*)?)', param)
        if match:
            op = match.group(1)
            val = float(match.group(5))
            if op == '>':
                return {'$gt': val}
            if op == '<':
                return {'$lt': val}
            if op == '>=':
                return {'$gte': val}
            if op == '<=':
                return {'$lte': val}
            return val
        return None

    @classmethod
    def metadata(cls, cursor=0, limit=10):
        """
        Select all metadata.
        """
        meta = list(
            cls.mongo.db.Structured.find(
                {},
                { '_id': 0 }
            ).skip(cursor).limit(limit)
        )

        next_cursor = cursor + limit if len(meta) == limit else None

        return next_cursor, meta

    @classmethod
    def metadata_by_story_id(cls, story_id, cursor=0, limit=10):
        """
        Given a story id, retrieve its metadata.
        """
        meta = list(
            cls.mongo.db.Structured.find(
                {'rp_story_id': story_id},
                {'_id': 0}
            ).skip(cursor).limit(limit)
        )

        next_cursor = cursor + limit if len(meta) == limit else None

        return next_cursor, meta

    @classmethod
    def metadata_by_entity_id(cls, entity_id=''):
        """
        Return the entity with the given id.
        """
        return cls.mongo.db.findOne(
            { 'rp_enitity_id': entity_id},
            { '_id': 0 }
        )

    @classmethod
    def search_meta(cls, params:dict, cursor=0, limit=10):
        if not params:
            return cls.stories()
        
        query = {}
        entity_name = params.get('entity_name', None)
        if entity_name:
            query['entity_name'] = entity_name
        score1 = params.get('Score1', '')
        modifier = cls._numeric_modifier(score1)
        if score1 and modifier:
            query['Score1'] = modifier
        score2 = params.get('Score2', '')
        modifier = cls._numeric_modifier(score2)
        if params.get('Score2', None):
            query['Score2'] = modifier
        if params.get('timestamp_utc', None):
            pass

        ids = list(cls.mongo.db.Structured.aggregate([
            { '$match': query },
            { '$group': { '_id': '$rp_story_id'} },
            { '$sort': { 'relevance': -1 } },
            { '$skip': cursor },
            { '$limit': limit }
        ]))

        next_cursor = cursor + limit if len(ids) == limit else None

        stories = []
        for id in ids:
            stories.extend(list(
                cls.mongo.db.Unstructured.find(
                    { 'rp_story_id': id['_id'] },
                    {'_id': 0}
                )
            ))

        return next_cursor, stories

    @classmethod
    def search_text(cls, params=None, cursor=0, limit=10):
        if not params:
            return cls.stories()

        text_search = params.get('text_search', '')
        stories = list(
            cls.mongo.db.Unstructured.find(
                {
                    '$text': { '$search': text_search }
                },
                {
                    '_id': 0
                }
            ).skip(cursor).limit(limit)
        )

        next_cursor = cursor + limit if len(stories) == limit else None

        return next_cursor, stories