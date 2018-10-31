from flask import Flask, jsonify
from sqlalchemy.orm import sessionmaker

from utils import settings
from utils.models import *

app = Flask(__name__)

@app.route("/api/users")
def index():
    session = sessionmaker(bind=engine)()
    results = session.query(User)\
        .limit(settings.PAGINATION_SIZE)\
        .all()
    results = [
        {
            'id': x.uid,
            'name': x.name,
            #'email': x.mail hidden for security
        }
        for x in results
    ]
    session.close()
    return jsonify(results)