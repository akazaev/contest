from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__, static_url_path='/upload')
    CORS(app)
    app.config.update(
        SECRET_KEY='123456'
    )

    from converter.web.routes import base
    app.register_blueprint(base.base)
    return app
