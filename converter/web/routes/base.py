import os
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
def send_js(uuid, page):
    return send_from_directory(os.path.join(UPLOAD_PATH, f'{uuid}/pages'),
                               f'{uuid}_{page}.jpg')


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
    return templating.render_template('main.html', documents=documents)
