from datetime import datetime
import logging
from multiprocessing import Process
import os
import subprocess
import time

import psutil

from converter import UPLOAD_PATH
from converter.db.managers import DocumentManager
from converter.nlp_utils import nlp_analysis
from pdf2image import convert_from_path


logger = logging.getLogger(__file__)


def convert2pdf(uuid, filename):
    DocumentManager.upsert({'uuid': uuid, 'status': 'new', 'pages': 0, 'ready': 0, 'msg': '',
                            'filename': filename, 'timestamp': datetime.now()})
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
            DocumentManager.upsert({'uuid': uuid}, {'status': 'pdf_failed', 'msg': stderr})
        else:
            DocumentManager.upsert({'uuid': uuid}, {'status': 'pdf'})

    source_pdf = '.'.join([os.path.splitext(source)[0], 'pdf'])
    os.rename(source_pdf, pdf_path)

    pages = []
    try:
        pages = convert_from_path(pdf_path, 300)
    except Exception as err:
        DocumentManager.upsert({'uuid': uuid},
                               {'status': 'jpg_failed', 'msg': str(err)})
    else:
        DocumentManager.upsert({'uuid': uuid}, {'ready': 0, 'pages': len(pages), 'status': 'jpg'})

    try:
        queue = []
        for i, page in enumerate(pages, start=1):
            queue.append((uuid, i))
            page.save(os.path.join(pages_path, f'{i}.jpg'), 'JPEG')
            DocumentManager.upsert({'uuid': uuid}, {'ready': i})
    except Exception as err:
        DocumentManager.upsert({'uuid': uuid},
                               {'status': 'jpg_failed', 'msg': str(err)})
        return
    else:
        DocumentManager.upsert({'uuid': uuid}, {'status': 'ready'})

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
