import logging
from logging import info

from flask import Flask, jsonify, request
from flask_restful import Resource, Api

from ta.data_management.data_sync import fetch_all_symbols_data
from ta.db.mongo_tools import get_symbols, add_symbol, delete_symbol, get_time_series

from multiprocessing import Process

app = Flask(__name__)
api = Api(app)


class SymbolsAdmin(Resource):
    def get(self):
        return jsonify([{'ticker': x.ticker} for x in get_symbols()])

    def post(self):
        content = request.get_json(silent=True)
        add_symbol(content)
        return self.get()

    def delete(self, ticker):
        delete_symbol(ticker)
        return self.get()

class SymbolsSync(Resource):
    def post(self):
        #Process(target=fetch_all_symbols_data).start()
        return "Synching Started"

class TimeSeries(Resource):
    def get(self):
        return get_time_series('SSO').to_csv()


api.add_resource(SymbolsAdmin, '/api/admin/symbols', '/api/admin/symbols/<string:ticker>')
api.add_resource(SymbolsSync, '/api/admin/symbols-sync', '/api/admin/symbols-sync/<string:ticker>')
api.add_resource(TimeSeries, '/api/time-series', '/api/time-series/<string:ticker>')

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

    app.run(host='0.0.0.0', debug=True, use_reloader=False)
