import codecs
import json
import logging

import requests
from bson.json_util import dumps
from flask import Flask, render_template, request, redirect, url_for, session
from flask import jsonify
from pymongo import MongoClient
import datetime
app = Flask(__name__)
logged_in = False

email_name =""
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


# [END form]
# [START submitted]
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
products = db["fs.files"]


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

    client = MongoClient("mongodb+srv://d:d@cluster0.ccyermz.mongodb.net/?retryWrites=true&w=majority")
    # connect to the db
    db = client.Shop
    collection = db.Items

    if request.method == "POST":
        item = request.form["item"]
        itemName = request.form["itemName"]

        print("HERE I AM", item, itemName)
        #insert_user = collection.insert_one(data)


    return render_template("shop.html", response=data["items"])


@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")

@app.route("/logged-in", methods=["POST"])
def logged_in():
    global logged_in, email_name
    output = request.get_json()
    #print(output)  # This is the output that was stored in the JSON within the browser
    #print(type(output))
    result = json.loads(output)  # this converts the json output to a python dictionary
     # this shows the json converted as a python dictionary
    email_name = result["firstname"]
    logged_in = True
    #print(email_name)
    prints()

    return result
def prints():
    print("prints function",email_name, logged_in)



@app.route("/write-reviews", methods=["GET", "POST"])
def writeReviews():
    return render_template("write-reviews.html")\


@app.route("/comments", methods=["GET", "POST"])
def comments():
    global name, review
    url = "https://europe-west2-river-psyche-366910.cloudfunctions.net/reviews"
    response = requests.get(url)
    responseString = response.content
    responseString = str(responseString)
    responseString = responseString[3:-2]

    responseString2 = "{\"items\":[" + responseString + "]}"
    data = json.loads(responseString2)

    client = MongoClient("mongodb+srv://d:d@cluster0.ccyermz.mongodb.net/?retryWrites=true&w=majority")
    # connect to the db
    db = client.Shop
    collection = db.reviews

    if request.method == "POST":
        name = request.form["name"]
        review = request.form["review"]
        date = str(datetime.datetime.now().strftime("%A %d-%m-%Y, %H:%M:%S"))
        data = {
            "name": name,
            "review": review,
            "reviewDate": date
        }
        insert_user = collection.insert_one(data)

    myCursor = db.reviews.find({})
    list_cur = list(myCursor)

    return render_template("comments.html", response=list_cur)

@app.route('/sign_out.html')
def sign_out():
    return render_template('sign_out.html')


@app.route("/admin", methods=["GET", "POST"])
def admin():
    url = "https://europe-west2-river-psyche-366910.cloudfunctions.net/shop-items"
    response = requests.get(url)
    responseString = response.content
    responseString = str(responseString)
    responseString = responseString[3:-2]

    responseString2 = "{\"items\":[" + responseString + "]}"
    data = json.loads(responseString2)
    client = MongoClient("mongodb+srv://d:d@cluster0.ccyermz.mongodb.net/?retryWrites=true&w=majority")
    db = client.Shop
    collection = db.Items

    # collection.find({name: itemName})


    if request.method == "POST":
        item = request.form["item"]
        itemName = request.form["itemName"]
        a = collection.find_one({"name": f"{itemName}"})
        print(item, itemName, a)
        myquery = {"name": f"{itemName}"}
        newvalues = {"$set": {"stock": f"{item}"}}

        collection.update_one(myquery, newvalues)
    return render_template("admin.html", response=data["items"])
@app.route('/test2')
def index():
    return render_template('test.html')
@app.route('/test', methods=['POST'])
def test():
    output = request.get_json()
    print(output) # This is the output that was stored in the JSON within the browser
    print(type(output))
    result = json.loads(output) #this converts the json output to a python dictionary
    print(result) # Printing the new dictionary
    print(type(result))#this shows the json converted as a python dictionary
    return result




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
