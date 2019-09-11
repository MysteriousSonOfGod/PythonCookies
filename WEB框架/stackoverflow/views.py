import ujson
from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html')


@app.route('/')
def questions():
    return render_template('questions.html')


@app.route('/update')
def update(timestamp=0):
    db = MongoClient("localhost", 27017)["stack_questions"]
    coll = db["questions"]
    records = coll.find({"fetched": {"$gt": timestamp}}).sort(
        "fetched", direction=-1)
    return ujson.dumps([e for e in records])


if __name__ == '__main__':
    app.run()
