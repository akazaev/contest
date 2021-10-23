import os
import json
import sqlite3
from threading import Thread
import uuid
from urllib.parse import urljoin

from flask import (
    Blueprint, request, redirect, templating, jsonify, send_from_directory)
from flask_wtf import FlaskForm, file

from converter import UPLOAD_PATH, DB
from converter.utils import convert2pdf


base = Blueprint('forms', __name__)


class UploadForm(FlaskForm):
    document = file.FileField(validators=[file.FileRequired()])


@base.route('/upload', methods=('GET', 'POST'))
def load_document():
    form = UploadForm()
    if form.validate_on_submit():
        doc_uuid = str(uuid.uuid4())
        doc_path = os.path.join(UPLOAD_PATH, doc_uuid)
        os.mkdir(doc_path)
        document = request.files['document']
        document.save(os.path.join(doc_path, document.filename))

        thread = Thread(target=convert2pdf, args=(doc_uuid, document.filename))
        thread.start()

        response = {
            'uuid': doc_uuid
        }
        return jsonify(response)

    return templating.render_template('form.html', form=form)


@base.route('/progress', methods=('GET',))
def get_progress():
    doc_id = request.args.get('uuid')

    connection = sqlite3.connect(DB)
    cursor = connection.cursor()
    cursor.execute(f"select pages, ready, status, msg from "
                   f"documents where uuid = '{doc_id}'")
    rows = cursor.fetchall()

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
    return send_from_directory(os.path.join(UPLOAD_PATH, f'{uuid}/pages'),
                               f'{uuid}_{page}.jpg')


@base.route('/nlp/<uuid>/<page>.json')
def load_nlp(uuid, page):
    if page.isdigit():
        page = int(page)
    else:
        page = int(page.split('_')[1])

    connection = sqlite3.connect(DB)
    cursor = connection.cursor()
    cursor.execute(f"select status, json from "
                   f"nlp where uuid = '{uuid}' and page = {page}")
    rows = cursor.fetchall()

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
    connection = sqlite3.connect(DB)
    cursor = connection.cursor()
    cursor.execute(f"select id, uuid, pages, ready, status, filename "
                   f"from documents order by id desc")
    rows = cursor.fetchall()
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
    rows = cursor.execute(f"select distinct uuid from nlp order by id desc").fetchall()
    for row in rows:
        uuid = row[0]
        document = cursor.execute(f"select id, filename, pages from documents where uuid = '{uuid}' order by id desc").fetchone()
        pages = cursor.execute(f"select id, page, status uuid from nlp where uuid = '{uuid}' order by page").fetchall()
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
