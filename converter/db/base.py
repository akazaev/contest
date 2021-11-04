from pymongo import MongoClient, ASCENDING, DESCENDING

from converter.config import MONGO_URL


_CLIENT = None


def get_client():
    global _CLIENT
    if not _CLIENT:
        _CLIENT = MongoClient(MONGO_URL)
    return _CLIENT


class DBManager:
    collection = model = None

    @classmethod
    def upsert(cls, key, data=None):
        assert isinstance(key, dict)
        data = data or key
        assert isinstance(data, dict)

        client = get_client()
        db = client.documents
        response = db[cls.collection].update(key, {'$set': data},
                                             upsert=True)
        return response

    @classmethod
    def insert(cls, data=None):
        client = get_client()
        db = client.documents
        if isinstance(data, dict):
            for key in data:
                if not hasattr(cls.model, key):
                    raise ValueError(f'unknown field {key}')
            db[cls.collection].insert(data)
        if isinstance(data, list):
            for key in data[0]:
                if not hasattr(cls.model, key):
                    raise ValueError(f'unknown field {key}')
            db[cls.collection].insert_many(data)

    @classmethod
    def remove(cls, data):
        client = get_client()
        db = client.documents
        db[cls.collection].remove(data)

    @classmethod
    def clear(cls):
        client = get_client()
        db = client.documents
        db[cls.collection].drop()

    @classmethod
    def get_first(cls, **kwargs):
        kwargs['first'] = True
        return cls.get(**kwargs)

    @classmethod
    def get(cls, **kwargs):
        sort = kwargs.pop('sort', None)
        first = kwargs.pop('first', False)
        fields = kwargs.pop('fields', {})
        if sort and not isinstance(sort, list):
            sort = [sort]

        client = get_client()
        db = client.documents
        if first:
            response = db[cls.collection].find_one(kwargs)
            response = dict(response)
            response.pop('_id', None)
            return cls.model(**response)
        else:
            if fields:
                response = db[cls.collection].find(kwargs, fields)
            else:
                response = db[cls.collection].find(kwargs)
            if sort:
                response = response.sort([
                    (field[0], ASCENDING if field[1] >= 0 else DESCENDING)
                    if isinstance(field, tuple) else (field, ASCENDING)
                    for field in sort])

            items = []
            for r in response:
                r = dict(r)
                r.pop('_id', None)
                items.append(cls.model(**r))
            return items
