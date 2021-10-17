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
    cursor.execute("create table if not exists documents"
                   " (uuid text, pages int, ready int,"
                   "status text, msg text);")
    cursor.execute(f"insert or replace into documents (uuid, status)"
                   f" values('{uuid}', 'new')")
    connection.commit()

    path = os.path.join(UPLOAD_PATH, uuid)
    pages_path = os.path.join(path, 'pages')
    os.mkdir(pages_path)
    source = os.path.join(path, filename)
    command = ['libreoffice', '--headless', '--convert-to',
               f'pdf:writer_pdf_Export', f"{source}", '--outdir', f"{path}"]
    logger.info(' '.join(command))
    process = subprocess.Popen(command,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    logger.info(stdout)
    logger.error(stderr)
    source_pdf = '.'.join([os.path.splitext(source)[0], 'pdf'])
    pdf_path = os.path.join(path, f'{uuid}.pdf')
    os.rename(source_pdf, pdf_path)
    cursor.execute(f"update documents set status = 'pdf' where "
                   f"uuid = '{uuid}'")
    connection.commit()

    pages = convert_from_path(pdf_path, 500)
    cursor.execute(f"update documents set ready = 0, pages = {len(pages)}, "
                   f"status = 'jpeg' where uuid = '{uuid}'")
    connection.commit()

    for i, page in enumerate(pages, start=1):
        page.save(os.path.join(pages_path, f'{uuid}_{i}.jpg'), 'JPEG')
        cursor.execute(f"update documents set ready = {i} where "
                       f"uuid = '{uuid}'")
        connection.commit()

    cursor.execute(f"update documents set  "
                   f"status = 'ready' where uuid = '{uuid}'")
    connection.commit()
