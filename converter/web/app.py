from flask import Flask


def create_app():
    app = Flask(__name__, static_url_path='/upload')
    app.config.update(
        SECRET_KEY='123456'
    )

    from converter.web.routes import base
    app.register_blueprint(base.base)
    return app
