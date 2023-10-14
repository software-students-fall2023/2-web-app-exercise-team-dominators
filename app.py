from flask import Flask, render_template, url_for
from pymongo import MongoClient

app = Flask(__name__)
# try using ATLAS for shared clusters,
# @Database name = ticket_monster, USer as tmpt collection name, first run works fine.
ATLAS_URI = "mongodb+srv://ys4323:Syysyysyy1!!@cluster0.ocmpb3f.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(ATLAS_URI)
db = client.ticket_monster


@app.route('/')
def index():
    data = db.USer.find()
    return render_template('index.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
