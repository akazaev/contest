from converter.db.base import DBManager
from converter.db.models import Document, Nlp, Exclude, Include


class DocumentManager(DBManager):
    collection = 'documents'
    model = Document


class NlpManager(DBManager):
    collection = 'nlp'
    model = Nlp


class ExcludeManager(DBManager):
    collection = 'exclude'
    model = Exclude


class IncludeManager(DBManager):
    collection = 'include'
    model = Include
