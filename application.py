from flask import Flask, jsonify
from sqlalchemy.orm import sessionmaker

from utils import settings
from utils.models import *

app = Flask(__name__)

@app.route("/")
def index():
    return 'Endpoints: <ul>{}</ul>'.format(''.join([
            '<li><a href="api/{0}">First 100 {0}</a></li>'.format(endpoint)
            for endpoint in ['users', 'groups']
        ]))

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
            'email': '- dedacted for now -'
        }
        for x in results
    ]
    session.close()
    return jsonify(results)

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
    return jsonify(results)