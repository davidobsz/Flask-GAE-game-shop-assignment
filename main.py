import codecs
import json
import logging

import requests
from bson.json_util import dumps
from flask import Flask, render_template, request, redirect, url_for, session
from flask import jsonify
from pymongo import MongoClient


app = Flask(__name__)
logged_in = False

@app.route('/')
@app.route('/home')
def home():
    print(logged_in)
    return render_template('home.html', logged_in=logged_in)


@app.route('/about', methods=["GET", "POST"])
def about():
    return render_template('about.html')


@app.route('/register', methods=["GET", "POST"])
def form():
    return render_template('register.html')


@app.route('/submitted', methods=["GET", "POST"])
def submitted_form():
    name = request.form['name']
    email = request.form['email']
    site = request.form['site_url']
    comments = request.form['comments']
    # [END submitted]
    # [START render_template]
    return render_template(
        'submitted_form.html',
        name=name,
        email=email,
        site=site,
        comments=comments)
    # [END render_template]


# -------------------------------------------
cluster = MongoClient("mongodb+srv://d:d@cluster0.ccyermz.mongodb.net/?retryWrites=true&w=majority")
db = cluster["Pythontest"]
collection = db["Students"]
products=db["fs.files"]





def get_mongodb_items():
    # Search data from Mongodb
    myCursor = None
    # create queries
    title_query = {"Unit title": {"$eq": "IoT Unit"}}
    author_query = {"Unit leader": {"$eq": "Xin"}}
    dateCreated_query = {"dateCreated": {"$eq": 2021}}
    myCursor = collection.find({"$and": [title_query, author_query, dateCreated_query]})
    list_cur = list(myCursor)
    print(list_cur)
    json_data = dumps(list_cur)
    return json_data


def store_mongodb(Unittitle, Unitleader, content, dateCreated, thumbnail):
    # Write to MongoDB
    json_data = {"Unit title": Unittitle, "Unit leader": Unitleader, "dateCreated": dateCreated, "thumbnail": thumbnail,
                 "content": content}
    collection.insert_one(json_data)


@app.route('/unit')
def Post_Mongo():
    store_mongodb('IoT Unit', 'Xin', 'Welcome to IoT Unit', 2021, ',')
    return "done"


@app.route('/display', methods=["GET", "POST"])
def display():
    jResponse = get_mongodb_items()
    data = json.loads(jResponse)
    return jsonify(data)


# cloud function <- test TEST TEST TEST
@app.route("/shop", methods=["GET", "POST"])
def hello():
    url = "https://europe-west2-river-psyche-366910.cloudfunctions.net/shop-items"
    response = requests.get(url)
    responseString = response.content
    responseString = str(responseString)
    responseString = responseString[3:-2]

    responseString2 = "{\"items\":[" + responseString + "]}"
    data = json.loads(responseString2)
    print(data)
    print(data["items"][0]["name"])
    itemArray = data["items"]
    print(itemArray[0])

    return render_template("shop.html", response=data["items"])

@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")

# -------------------------------------------

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    # Only run for local development.
    app.run(host='127.0.0.1', port=8080, debug=True)
