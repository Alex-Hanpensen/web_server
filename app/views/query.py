from flask_restx import Resource, Namespace
from flask import request

query_ns = Namespace('/perform_query')


@query_ns.route('/')
class QueryView(Resource):
    def post(self):
        data = request.json
