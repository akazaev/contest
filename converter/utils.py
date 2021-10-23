import logging
import multiprocessing
import os
import subprocess
import sqlite3

from converter import UPLOAD_PATH, DB
from converter.nlp import process_nlp
from pdf2image import convert_from_path


logger = logging.getLogger(__file__)


def convert2pdf(uuid, filename):
    connection = sqlite3.connect(DB)
    cursor = connection.cursor()
    cursor.execute(f"insert or replace into documents (uuid, status, filename)"
                   f" values('{uuid}', 'new', '{filename}')")
    connection.commit()

    path = os.path.join(UPLOAD_PATH, uuid)
    pages_path = os.path.join(path, 'pages')
    os.mkdir(pages_path)
    source = os.path.join(path, filename)
    pdf_path = os.path.join(path, f'{uuid}.pdf')

    ext = os.path.splitext(source)[1]
    print(ext.lower())
    if ext.lower() != '.pdf':
        command = ['libreoffice', '--headless', '--convert-to',
                   f'pdf:writer_pdf_Export', f"{source}",
                   '--outdir', f"{path}"]
        process = subprocess.Popen(command, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        _stdout, stderr = process.communicate()

        if process.returncode:
            cursor.execute(f"update documents set status = 'pdf_failed',"
                           f"msg = '{stderr}' where uuid = '{uuid}'")
        else:
            cursor.execute(f"update documents set status = 'pdf' where "
                           f"uuid = '{uuid}'")
        connection.commit()

    source_pdf = '.'.join([os.path.splitext(source)[0], 'pdf'])
    os.rename(source_pdf, pdf_path)

    pages = []
    try:
        pages = convert_from_path(pdf_path, 300)
    except Exception as err:
        cursor.execute(f"update documents set status = 'jpg_failed',"
                       f"msg = '{str(err)}' where uuid = '{uuid}'")
    else:
        cursor.execute(f"update documents set ready = 0, pages = {len(pages)},"
                       f"status = 'jpg' where uuid = '{uuid}'")
    connection.commit()

    try:
        queue = []
        for i, page in enumerate(pages, start=1):
            queue.append((uuid, i))
            page.save(os.path.join(pages_path, f'{i}.jpg'), 'JPEG')
            cursor.execute(f"update documents set ready = {i} where uuid = '{uuid}'")
    except Exception as err:
        cursor.execute(
            f"update documents set status = 'jpg_failed', msg = '{str(err)}' where uuid = '{uuid}'")
    else:
        cursor.execute(f"update documents set  "
                       f"status = 'ready' where uuid = '{uuid}'")
        connection.commit()
        connection.close()

        with multiprocessing.Pool() as pool:
            pool.map(process_nlp, queue)
