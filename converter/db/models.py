from collections import namedtuple


Document = namedtuple('Document', ['uuid', 'pages', 'ready', 'status',
                                   'msg', 'filename', 'timestamp'])

Nlp = namedtuple('Nlp', ['uuid', 'page', 'status', 'json',
                         'final', 'timestamp'])

Exclude = namedtuple('Exclude', ['word'])

Include = namedtuple('Include', ['word'])
