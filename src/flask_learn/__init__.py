import os
from typing import Mapping, Any
from logging.config import dictConfig
import logging

from flask import Flask, render_template

from .logger import dict_config

dictConfig(dict_config)
error_logger = logging.getLogger('error')


def create_app(test_config: Mapping[str, Any] | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flask.sqlite'),
    )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db

    db.init_app(app)

    from . import auth, blog

    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)

    app.add_url_rule('/', endpoint='index')

    app.register_error_handler(404, handle_404)
    app.register_error_handler(400, handle_400)
    app.register_error_handler(500, handle_500)

    @app.errorhandler(Exception)
    def handle_other(error):
        error_logger.error(f'{error}', exc_info=True)
        return render_template('500.html', error=error), 500

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app


def handle_404(error):
    return render_template('404.html', error=error), 404


def handle_400(error):
    return render_template('400.html', error=error), 400


def handle_500(error):
    return render_template('500.html', error=error), 500
