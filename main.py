from flask import Flask
from flask_restx import Api
from app.config import Config
from app.views.query import query_ns


def create_app(config: Config) -> Flask:
    """
    creating an application
    :param config:
    :return: Flask
    """
    application = Flask(__name__)
    application.config.from_object(config)
    application.app_context().push()
    return application


def register_extensions(application: Flask) -> None:
    """
    added a rout
    :param application:
    :return: None
    """
    api = Api(application)
    api.add_namespace(query_ns)


if __name__ == '__main__':
    app = create_app(Config())
    register_extensions(app)
    app.run()
