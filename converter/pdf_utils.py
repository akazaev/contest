import logging
from multiprocessing import Process
import os
import subprocess
import time

import psutil

from converter import UPLOAD_PATH, db
from converter.nlp_utils import nlp_analysis
from pdf2image import convert_from_path


logger = logging.getLogger(__file__)


def convert2pdf(uuid, filename):
    with db.db() as connection:
        connection.execute(f"insert or replace into documents (uuid, status, filename)"
                           f" values('{uuid}', 'new', '{filename}')")

    path = os.path.join(UPLOAD_PATH, uuid)
    pages_path = os.path.join(path, 'pages')
    os.mkdir(pages_path)
    source = os.path.join(path, filename)
    pdf_path = os.path.join(path, f'{uuid}.pdf')

    ext = os.path.splitext(source)[1]
    if ext.lower() != '.pdf':
        command = ['libreoffice', '--headless', '--convert-to',
                   f'pdf:writer_pdf_Export', f"{source}",
                   '--outdir', f"{path}"]
        process = subprocess.Popen(command, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        _stdout, stderr = process.communicate()

        if process.returncode:
            with db.db() as connection:
                connection.execute(f"update documents set status = 'pdf_failed',"
                                   f"msg = '{stderr}' where uuid = '{uuid}'")
        else:
            with db.db() as connection:
                connection.execute(f"update documents set status = 'pdf' where "
                                   f"uuid = '{uuid}'")

    source_pdf = '.'.join([os.path.splitext(source)[0], 'pdf'])
    os.rename(source_pdf, pdf_path)

    pages = []
    try:
        pages = convert_from_path(pdf_path, 300)
    except Exception as err:
        with db.db() as connection:
            connection.execute(f"update documents set status = 'jpg_failed',"
                               f"msg = '{str(err)}' where uuid = '{uuid}'")
    else:
        with db.db() as connection:
            connection.execute(f"update documents set ready = 0, pages = {len(pages)},"
                               f"status = 'jpg' where uuid = '{uuid}'")

    try:
        queue = []
        for i, page in enumerate(pages, start=1):
            queue.append((uuid, i))
            page.save(os.path.join(pages_path, f'{i}.jpg'), 'JPEG')
            with db.db() as connection:
                connection.execute(f"update documents set ready = {i} where uuid = '{uuid}'")
    except Exception as err:
        with db.db() as connection:
            connection.execute(f"update documents set status = 'jpg_failed', msg = '{str(err)}' where uuid = '{uuid}'")
    else:
        with db.db() as connection:
            connection.execute(f"update documents set status = 'ready' where uuid = '{uuid}'")

        cpu_count = psutil.cpu_count(logical=False) - 1
        jobs = {}
        while queue:
            remove = []
            for data, thread in jobs.items():
                if not thread.is_alive():
                    remove.append(data)
            for data in remove:
                jobs.pop(data)
            if len(jobs) < cpu_count:
                for i in range(cpu_count - len(jobs)):
                    if not queue:
                        break
                    uuid, page = queue.pop(0)
                    thread = Process(target=nlp_analysis, args=(uuid, page))
                    thread.start()
                    jobs[(uuid, page)] = thread
            time.sleep(2)


if __name__ == '__main__':
    convert2pdf('', '')
