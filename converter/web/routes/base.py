import os
import json
import multiprocessing
import uuid
from urllib.parse import urljoin

from flask import Blueprint, request, templating, jsonify, send_from_directory
from flask_wtf import FlaskForm, file

from converter import UPLOAD_PATH, db
from converter.pdf_utils import convert2pdf
from converter.image_utils import process_data


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

        thread = multiprocessing.Process(target=convert2pdf, args=(doc_uuid, document.filename))
        thread.start()

        response = {
            'uuid': doc_uuid
        }
        return jsonify(response)

    return templating.render_template('form.html', form=form)


@base.route('/progress', methods=('GET',))
def get_progress():
    doc_id = request.args.get('uuid')

    with db.db() as connection:
        connection.execute(f"select pages, ready, status, msg from "
                           f"documents where uuid = '{doc_id}'")
        rows = connection.fetchall()

    response = {'uuid': doc_id, 'files': [], 'pages': None,
                'ready': None, 'status': None, 'message': ''}
    if rows:
        pages, ready, status, msg = rows[0]
        response['pages'] = pages
        response['ready'] = ready
        response['status'] = status
        response['message'] = msg
        if pages is not None:
            response['files'] = [
                urljoin(request.host_url, f'file/{doc_id}/{i + 1}.jpg')
                for i in range(pages)
            ]
    return jsonify(response)


@base.route('/file/<uuid>/<page>.jpg')
def load_page(uuid, page):
    return send_from_directory(os.path.join(UPLOAD_PATH, f'{uuid}/pages'), f'{page}.jpg')


@base.route('/file/<uuid>/<page>_new.jpg')
def load_new_page(uuid, page):
    return send_from_directory(os.path.join(UPLOAD_PATH, f'{uuid}/pages'), f'{page}_new.jpg')


@base.route('/nlp/<uuid>/<page>')
def load_nlp(uuid, page):
    if page.isdigit():
        page = int(page)
    else:
        page = int(page.split('_')[1])

    with db.db() as connection:
        connection.execute(f"select status, json from "
                       f"nlp where uuid = '{uuid}' and page = {page}")
        rows = connection.fetchall()

    response = {'uuid': uuid, 'page': page, 'status': None, 'boxes': None}
    if rows:
        status, boxes = rows[0]
        response['status'] = status
        if boxes:
            boxes = json.loads(boxes)
            response['boxes'] = boxes
    else:
        response['status'] = 'not_found'
    return jsonify(response)


@base.route('/', methods=('GET', ))
def main():
    with db.db() as connection:
        connection.execute(f"select id, uuid, pages, ready, status, filename "
                           f"from documents order by id desc")
        rows = connection.fetchall()
    documents = []
    for row in rows:
        id, uuid, pages, ready, status, filename = row
        documents.append({
            'id': id,
            'uuid': uuid,
            'pages': pages or '?',
            'ready': ready or '?',
            'status': status,
            'filename': filename or uuid,
        })

    nlp = []
    with db.db() as connection:
        rows = connection.execute(f"select distinct uuid from nlp order by id desc").fetchall()
        for row in rows:
            uuid = row[0]
            document = connection.execute(f"select id, filename, pages from documents where uuid = '{uuid}' order by id desc").fetchone()
            pages = connection.execute(f"select id, page, status uuid from nlp where uuid = '{uuid}' order by page").fetchall()
            data = []
            for page in pages:
                data.append({
                    'id': page[0],
                    'page': page[1],
                    'status': page[2],
                })
            nlp.append({
                'id': document[0],
                'uuid': uuid,
                'filename': document[1],
                'pages': document[2],
                'data': data
            })

    return templating.render_template('main.html', documents=documents, nlp=nlp)


@base.route('/include', methods=('POST', ))
def include_words():
    data = request.json
    words = data.get('words', [])
    with db.db() as connection:
        for word in words:
            word = word.lower()
            connection.execute(f"insert into 'include' (word) values('{word}');")
            connection.execute(f"delete from 'exclude' where word = '{word}'")
    return jsonify({'result': 'ok'})


@base.route('/exclude', methods=('POST', ))
def exclude_words():
    data = request.json
    words = data.get('words', [])
    with db.db() as connection:
        for word in words:
            word = word.lower()
            connection.execute(f"insert into 'exclude' (word) values('{word}');")
            connection.execute(f"delete from 'include' where word = '{word}'")
    return jsonify({'result': 'ok'})


@base.route('/process/<uuid>/<page>', methods=('POST', ))
def process_data(uuid, page):
    data = request.json
    boxes = data.get('boxes', {})
    nlp = boxes.get('nlp', [])
    data = {'boxes': nlp}

    with db.db() as connection:
        connection.execute(f"update nlp set status = 'updated', final = '{json.dumps(data)}' where "
                           f"uuid = '{uuid}' and page = {page}")
        for box in nlp:
            word = box['text'].lower()
            connection.execute(f"insert into 'exclude' (word) values('{word}');")
            connection.execute(f"delete from 'include' where word = '{word}'")

    thread = multiprocessing.Process(target=process_data,
                                     args=(uuid, page, data))
    thread.start()
    return jsonify({'result': 'ok'})
