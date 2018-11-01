from flask import Flask, jsonify, send_from_directory
from sqlalchemy.orm import sessionmaker

from config import settings
from utils.models import *

app = Flask(__name__)

def _jsonify(blob):
    return jsonify(blob)
    return jsonify(blob.encode('utf-8').strip())

@app.route("/")
def index():
    return 'Basic api endpoints we have working: <ul>{}</ul>{}'.format(''.join([
            '<li><a href="api/{0}">First 100 {0}</a></li>'.format(endpoint)
            for endpoint in ['users', 'groups']
        ]), '<a href="./frontend/index.html">Or try our fancy interface</a>')

@app.route('/frontend/<path:path>')
def send_js(path):
    return send_from_directory('frontend', path)

@app.route("/api/users")
def api_users():
    session = sessionmaker(bind=engine)()
    results = session.query(User)\
        .limit(settings.PAGINATION_SIZE)\
        .all()
    results = [
        {
            'id': x.id,
            'name': x.name,
            'email': 'redacted_for_now'
        }
        for x in results
    ]
    session.close()
    return _jsonify(results)

@app.route("/api/groups")
def api_groups():
    session = sessionmaker(bind=engine)()
    results = session.query(Group)\
        .limit(settings.PAGINATION_SIZE)\
        .all()
    results = [
        {
            'id': x.id,
            'name': x.name,
        }
        for x in results
    ]
    session.close()
    return _jsonify(results)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
