from flask import Flask, jsonify, request
from flask_cors import CORS

from ta.db.mongo_tools import get_symbols, add_symbol

app = Flask(__name__, static_url_path='')
CORS(app)


@app.route('/api/admin/symbols', methods=['GET', 'POST', 'OPTION'])
def admin_symbols():
    if request.method == 'POST':
        content = request.get_json(silent=True)
        add_symbol(content)
    return jsonify([{'ticker': x['ticker']} for x in get_symbols()])

if __name__ == "__main__":
    app.run(host='0.0.0.0')
