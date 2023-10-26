from flask_restx import Resource, Namespace
from flask import request
import json

from service import WebServer

query_ns = Namespace('/perform_query')


@query_ns.route('/')
class QueryView(Resource):
    def post(self):
        return '\n'.join([data for data in WebServer(**dict(request.args)).get_start()])
