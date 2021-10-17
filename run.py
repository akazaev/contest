import os

from converter import UPLOAD_PATH
from converter.web.app import create_app


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_PATH):
        os.mkdir(UPLOAD_PATH)

    app = create_app()
    app.run(debug=True)
