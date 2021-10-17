import logging
import os
import subprocess
import sqlite3

from converter import UPLOAD_PATH, DB
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
    if ext.lower() != 'pdf':
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
        pages = convert_from_path(pdf_path, 500)
    except Exception as err:
        cursor.execute(f"update documents set status = 'jpg_failed',"
                       f"msg = '{str(err)}' where uuid = '{uuid}'")
    else:
        cursor.execute(f"update documents set ready = 0, pages = {len(pages)},"
                       f"status = 'jpg' where uuid = '{uuid}'")
    connection.commit()

    for i, page in enumerate(pages, start=1):
        try:
            page.save(os.path.join(pages_path, f'{uuid}_{i}.jpg'), 'JPEG')
        except Exception as err:
            cursor.execute(f"update documents set status = 'jpg_failed',"
                           f"msg = '{str(err)}' where uuid = '{uuid}'")
        else:
            cursor.execute(f"update documents set ready = {i} where "
                           f"uuid = '{uuid}'")
        connection.commit()

    cursor.execute(f"update documents set  "
                   f"status = 'ready' where uuid = '{uuid}'")
    connection.commit()
