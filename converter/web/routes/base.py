import os
import json
from multiprocessing import Process
import uuid
from urllib.parse import urljoin

from flask import Blueprint, request, templating, jsonify, send_from_directory
from flask_wtf import FlaskForm, file

from converter import UPLOAD_PATH
from converter.db.managers import (
    DocumentManager, NlpManager, ExcludeManager, IncludeManager)
from converter.pdf_utils import convert2pdf
from converter.image_utils import process_image


base = Blueprint('forms', __name__)


class UploadForm(FlaskForm):
    document = file.FileField(validators=[file.FileRequired()])

    def validate(self):
        return True


@base.route('/upload', methods=('GET', 'POST'))
def load_document():
    form = UploadForm()
    if form.validate_on_submit():
        doc_uuid = str(uuid.uuid4())
        doc_path = os.path.join(UPLOAD_PATH, doc_uuid)
        os.mkdir(doc_path)
        document = request.files['document']
        document.save(os.path.join(doc_path, document.filename))

        thread = Process(target=convert2pdf, args=(doc_uuid, document.filename))
        thread.start()

        response = {
            'uuid': doc_uuid
        }
        return jsonify(response)

    return templating.render_template('form.html', form=form)


@base.route('/progress', methods=('GET',))
def get_progress():
    doc_id = request.args.get('uuid')

    document = DocumentManager.get_first(uuid=doc_id)
    response = {'uuid': doc_id, 'files': [], 'pages': None,
                'ready': None, 'status': None, 'message': ''}
    if document:
        response['pages'] = document['pages']
        response['ready'] = document['ready']
        response['status'] = document['status']
        response['message'] = document['msg']
        if document['pages'] is not None:
            response['files'] = [
                urljoin(request.host_url, f'file/{doc_id}/{i + 1}.jpg')
                for i in range(document['pages'])
            ]
    return jsonify(response)


@base.route('/file/<uuid>/<page>.jpg')
def load_page(uuid, page):
    return send_from_directory(os.path.join(
        UPLOAD_PATH, f'{uuid}/pages'), f'{page}.jpg')


@base.route('/file/<uuid>/<page>_new.jpg')
def load_new_page(uuid, page):
    return send_from_directory(os.path.join(
        UPLOAD_PATH, f'{uuid}/pages'), f'{page}_new.jpg')


@base.route('/nlp/<uuid>/<page>')
def load_nlp(uuid, page):
    page = int(page)

    nlp = NlpManager.get_first(uuid=uuid, page=page)
    response = {'uuid': uuid, 'page': page, 'status': None, 'boxes': None}
    if nlp:
        response['status'] = nlp['status']
        if nlp['json']:
            boxes = json.loads(nlp['json'])
            response['boxes'] = boxes
    else:
        response['status'] = 'not_found'
    return jsonify(response)


@base.route('/', methods=('GET', ))
def main():
    documents = []
    for document in DocumentManager.get(sort=[('timestamp', -1)]):
        documents.append({
            'uuid': document['uuid'],
            'pages': document['pages'] or '?',
            'ready': document['ready'] or '?',
            'status': document['status'],
            'filename': document['filename'] or document['uuid'],
            'timestamp': document['timestamp'],
        })

    nlp = []
    nlps = NlpManager.get(sort=[('timestamp', -1)])
    uuids = {nlp['uuid'] for nlp in nlps}
    for uuid in uuids:
        document = DocumentManager.get_first(uuid=uuid)
        if not document:
            continue
        pages = NlpManager.get(uuid=uuid, sort=[('page', 1)])
        if not pages:
            continue
        data = []
        for page in pages:
            data.append({
                'page': page['page'],
                'status': page['status'],
            })
        nlp.append({
            'uuid': uuid,
            'filename': document['filename'],
            'pages': document['pages'],
            'data': data,
            'timestamp': document['timestamp'],
        })
        nlp = sorted(nlp, key=lambda x: x['timestamp'], reverse=True)

    return templating.render_template('main.html', documents=documents, nlp=nlp)


@base.route('/include', methods=('POST', ))
def include_words():
    data = request.json
    words = data.get('words', [])
    for word in words:
        word = word.lower()
        IncludeManager.upsert({'word': word})
        ExcludeManager.remove({'word': word})
    return jsonify({'result': 'ok'})


@base.route('/exclude', methods=('POST', ))
def exclude_words():
    data = request.json
    words = data.get('words', [])
    for word in words:
        word = word.lower()
        IncludeManager.remove({'word': word})
        ExcludeManager.upsert({'word': word})
    return jsonify({'result': 'ok'})


@base.route('/process/<uuid>/<page>', methods=('POST', ))
def process_data(uuid, page):
    data = request.json
    boxes = data.get('boxes', {})
    nlp = boxes.get('nlp', [])
    data = {'boxes': {'nlp': nlp}}
    page = int(page)

    NlpManager.upsert({"uuid": uuid, "page": page},
                      {"status": "updated", "final": json.dumps(data)})
    after = set()
    for box in nlp:
        word = box['text'].lower()
        IncludeManager.upsert({'word': word})
        ExcludeManager.remove({'word': word})
        after.add(word)

    before = set()
    nlp = NlpManager.get_first(uuid=uuid, page=page)
    boxes = json.loads(nlp['json'])
    words = boxes['nlp']
    for word in words:
        propn = word['propn']
        if propn:
            before.add(word['text'].lower())
    for word in before - after:
        ExcludeManager.upsert({'word': word})

    thread = Process(target=process_image, args=(uuid, page, data))
    thread.start()
    return jsonify({'result': 'ok'})
