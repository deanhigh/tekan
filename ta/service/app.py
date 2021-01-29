from flask import Flask, jsonify, request
from flask_restful import Resource, Api

from ta.db.mongo_tools import get_symbols, add_symbol, delete_symbol

app = Flask(__name__)
api = Api(app)


class SymbolsAdmin(Resource):
    def get(self):
        return jsonify([{'ticker': x['ticker']} for x in get_symbols()])

    def post(self):
        content = request.get_json(silent=True)
        add_symbol(content)
        return self.get()

    def delete(self, ticker):
        delete_symbol(ticker)
        return self.get()

class SymbolsSync(Resource):
    def post(self):
        print("Sync")
        return "Synching"

api.add_resource(SymbolsAdmin, '/api/admin/symbols', '/api/admin/symbols/<string:ticker>')
api.add_resource(SymbolsSync, '/api/admin/symbols-sync', '/api/admin/symbols-sync/<string:ticker>')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, use_reloader=False)
