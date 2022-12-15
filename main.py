# Import necessary modules
import codecs
import json
import logging
import requests
from bson.json_util import dumps
from flask import Flask, render_template, request, redirect, url_for, session
from flask import jsonify
from pymongo import MongoClient
import datetime
import os
import stripe

# Create a Flask app instance
app = Flask(__name__)
app.config['PREFERRED_URL_SCHEME'] = 'https'
# Initialize the "logged_in", "email_name" and "Stripe API key" variables
logged_in = False
email_name = ""
stripe.api_key = "rk_test_51MEg5JD68JztsQwgsOWYza5hLUE1cdK9haRBoXTrcnm2M1SAGbSDb5xSiQG5x8J2u5OaWhb4O0ZIm5VjGkojIKKy00XaSLfk6L"

# Initialise the MongoDB
# Connect to the MongoDB cluster and get the "Shop" database
client = MongoClient("mongodb+srv://d:d@cluster0.ccyermz.mongodb.net/?retryWrites=true&w=majority")
# Connect to the Shop db
db = client.Shop


# Define a route for "/" and "/home" URLs
@app.route('/')
@app.route('/home')
def home():
    print(logged_in)
    # Render the "home.html" template
    return render_template('home.html')


# Define a route for the "/about" URL
@app.route('/about', methods=["GET", "POST"])
def about():
    return render_template('about.html')

# -------------------------------------------

# Define the /shop route and view function allowing both GET and POST methods
@app.route("/shop", methods=["GET", "POST"])
def shop():
    # Set the URL for the shop-items cloud function
    url = "https://europe-west2-river-psyche-366910.cloudfunctions.net/shop-items"

    # Make a GET request to the URL and get the response
    response = requests.get(url)

    # Convert the response content to a string
    responseString = response.content
    responseString = str(responseString)

    # Remove the first and last characters from the response string
    responseString = responseString[3:-2]

    # Create a new string that contains the response data in a JSON array
    responseString2 = "{\"items\":[" + responseString + "]}"

    # Load the JSON data into a Python dictionary
    data = json.loads(responseString2)

    # If the request method is POST, get the product and email & product values
    # from the request form and insert them into the "basket" collection
    if request.method == "POST":
        product = request.form["product"]
        emailusername = request.form["emailusername"]
        collection = db.basket
        collection.insert_one({"email": f"{emailusername}", "product": f"{product}"})

    # Render the shop.html template, passing the products data to the template
    return render_template("shop.html", response=data["items"])


# Define the /login route and render login.html template
@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")


# Define the /logged route and view function allowing POST method
@app.route("/logged-in", methods=["POST"])
def logged_in_fun():
    # set global variable
    global logged_in, email_name

    # get the JSON data from the POST request which is made when the user has a successful sign in
    output = request.get_json()
    # convert the JSON output to a Python dictionary
    result = json.loads(output)

    # set email_name as the email of the user which successfully signed on. Data comes from ^ JSON request
    email_name = result["firstname"]
    logged_in = True

    # Set environment variables
    os.environ['email'] = email_name

    print("email_name", email_name)

    # Return the result as JSON
    return result


# Define the /write-reviews route and view function allowing POST and GET method
@app.route("/write-reviews", methods=["GET", "POST"])
def writeReviews():
    # render the write-reviews.html template
    return render_template("write-reviews.html")


# Define the /comments route and view function allowing POST and GET method
@app.route("/comments", methods=["GET", "POST"])
def comments():
    # Set the URL for the reviews cloud function
    url = "https://europe-west2-river-psyche-366910.cloudfunctions.net/reviews"
    response = requests.get(url)
    responseString = response.content
    responseString = str(responseString)
    responseString = responseString[3:-2]

    responseString2 = "{\"items\":[" + responseString + "]}"
    data = json.loads(responseString2)

    # Connect to Reviews db
    collection = db.reviews

    # if request is POST get data from the request -> format it as a python dictionary and insert into database
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

    # get reviews from the database
    myCursor = db.reviews.find({})
    list_cur = list(myCursor)

    # render the comments.html template with the reviews data
    return render_template("comments.html", response=list_cur)


# Define the /sign-out route
@app.route('/sign_out.html')
def sign_out():
    return render_template('sign_out.html')


# Define the /admin route and view function allowing POST and GET method
@app.route("/admin", methods=["GET", "POST"])
def admin():
    # Set the URL for the shop-items cloud function and get the data -> format the string into JSON then into python dict
    url = "https://europe-west2-river-psyche-366910.cloudfunctions.net/shop-items"
    response = requests.get(url)
    responseString = response.content
    responseString = str(responseString)
    responseString = responseString[3:-2]

    responseString2 = "{\"items\":[" + responseString + "]}"
    data = json.loads(responseString2)

    # Connect to Items db
    collection = db.Items

    # If request method is post get the form data from /admin
    if request.method == "POST":
        item = request.form["item"]
        itemName = request.form["itemName"]
        # if item and itemName are not null / have values
        if item and itemName:
            # Find the specific item in the database
            a = collection.find_one({"name": f"{itemName}"})
            print(item, itemName, a)
            myquery = {"name": f"{itemName}"}

            # update the stock of the specific item
            newvalues = {"$set": {"stock": f"{item}"}}
            collection.update_one(myquery, newvalues)

    # render the admin.html template with the data
    return render_template("admin.html", response=data["items"])


# /add items has GET and POST request. This function will add whole products to the Items collection of the shop database
@app.route("/add_items", methods=["GET", "POST"])
def addItems():
    # connect to the Items database
    collection = db.Items

    if request.method == "POST":
        # get data from the request
        name = request.form["name"]
        price = request.form["price"]
        bluetooth = request.form["bluetooth"]
        img = request.form["img"]
        cpu = request.form["cpu"]
        releaseDate = request.form["releaseDate"]
        storage = request.form["storage"]
        ram = request.form["ram"]
        stock = request.form["stock"]
        gpu = request.form["gpu"]

        # insert the item/product into the database
        collection.insert_one({
            "name": f"{name}",
            "price": f"{price}",
            "bluetooth": f"{bluetooth}",
            "img": f"{img}",
            "cpu": f"{cpu}",
            "releaseDate": f"{releaseDate}",
            "storage": f"{storage}",
            "ram": f"{ram}",
            "stock": f"{stock}",
            "gpu": f"{gpu}"
        })

    return render_template("add_items.html")


# /delete_items consists of POST and GET request. This route and function shows all the products and allows the admin to
# delete products from the Items collection
@app.route("/delete_items", methods=["POST", "GET"])
def deleteItems():
    # Connect to the shop-items cloud function URL and get the data -> make it into python dict
    url = "https://europe-west2-river-psyche-366910.cloudfunctions.net/shop-items"
    response = requests.get(url)
    responseString = response.content
    responseString = str(responseString)
    responseString = responseString[3:-2]

    responseString2 = "{\"items\":[" + responseString + "]}"
    data = json.loads(responseString2)

    # Connect to the Items database
    collection = db.Items

    # if request method is POST
    if request.method == "POST":
        # get item from the request
        item = request.form["item"]

        # delete the item based on its name
        collection.delete_one({"name": f"{item}"})

    # render the delete_items template with the data of the shop items
    return render_template("delete_items.html", response=data["items"])


# /delete_items consists of POST and GET request. This route and function shows all of the
# items within the logged-in users' basket.
@app.route("/basket", methods=["GET", "POST"])
def basket():
    # Connect to get-basket-items google cloud functions URL and make the response into python dict
    url = "https://europe-west2-river-psyche-366910.cloudfunctions.net/get-basket-items"
    response = requests.get(url)
    responseString = response.content
    responseString = str(responseString)
    responseString = responseString[3:-2]
    responseString2 = "{\"items\":[" + responseString + "]}"
    data = json.loads(responseString2)
    product_list = []

    # Connect to MongoDB databse to be able to query the database and remove things from
    # Basket on press of delete button
    collection = db.basket

    # This code below takes the email and product from the post request and deletes it from the MongoDB
    if request.method == "POST":
        email = request.form["email"]
        product = request.form["product"]
        print(email, product)
        collection.delete_one({"email": f"{email}", "product": f"{product}"})

    # render basket.html and send the list of products in the currently logged-in users basket
    return render_template("basket.html", response=data)


# Sets up payment based on what is clicked in the "buy" on the /shop route
@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    # If request method is POST, i.e., If user presses "buy" button in basket
    if request.method == "POST":
        product = request.form["product"]
        print(product)
        collection = db.Items

        # Find item based on name from the DB that the user pressed "buy" on from the basket
        result = collection.find_one({"name": f"{product}"})

        # Make the result into an int.
        price = result["price"]
        price = price.split(".")
        price = f"{price[0]}{price[1]}"
        print(price, "PRICE")

        # Create a stripe checkout session, with the product the user will buy
        # information coming from the db
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': f'{product}',
                    },
                    'unit_amount': int(price),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://localhost:4242/success',
            cancel_url='http://localhost:4242/cancel',
        )
        # redirect to the payment url
        return redirect(session.url, code=303)
    return "404.html"


# handles 500 error and returns exception.
@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500


# handles 404 errors returns 404.html
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# Application Default credentials are automatically created.


if __name__ == '__main__':
    # Only run for local development.
    app.run(host='127.0.0.1', port=8080, debug=True)
