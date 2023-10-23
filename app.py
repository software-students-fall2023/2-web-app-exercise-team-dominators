from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
# from faker import Faker
import random
import logging
from datetime import datetime


app = Flask(__name__)

# Setting up logging
logging.basicConfig(level=logging.DEBUG)
app.secret_key = "team_dominators"
# MongoDB connection string
ATLAS_URI = "mongodb+srv://ys4323:Syysyysyy1@cluster0.ocmpb3f.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(ATLAS_URI)
db = client.Ticket_monster
# fake = Faker()
# event_date = datetime.combine(fake.date_this_decade(), datetime.min.time())

# fetch events and users info from mongodb
events = db['Event']
users = db['USer']

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = users.find_one({"email": email, "password_hash": password})
        if user:
            session["logged_in"] = True
            return redirect(url_for("home"))
        else:
            return "Invalid credentials, please try again."

    return render_template("login.html")


@app.route('/home')
def home():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    
    featured_events = events.find().limit(20)



    return render_template("home.html", featured_events=featured_events)


# @app.route('/generate-data')
# def generate_data():
#     try:
#         # Generate and add random users
#         for _ in range(10):  # Generate 10 users
#             user = {
#                 "username": fake.user_name(),
#                 "email": fake.email(),
#                 "password_hash": fake.password(length=10),
#                 "watchlist": [],
#                 "notifications": []
#             }
#             db.USer.insert_one(user)

#         # Generate and add random events
#         event_ids = []  # Store generated event_ids
#         for _ in range(5):  # Generate 5 events
#             event_date = datetime.combine(
#                 fake.date_this_decade(), datetime.min.time())
#             event = {
#                 "event_name": fake.company(),
#                 "event_date": event_date,
#                 "venue": fake.address(),
#                 "available_tickets": random.randint(10, 500),
#                 "price": round(random.uniform(10, 500), 2),
#                 "description": fake.text(),
#                 "genre/category": fake.job(),
#                 "artists/teams": fake.name()
#             }
#             result = db.Event.insert_one(event)
#             event_ids.append(result.inserted_id)

#         return "Data generated and added successfully!"

#     except Exception as e:
#         logging.error(f"Error generating data: {e}")
#         return f"Error generating data: {e}", 500


if __name__ == '__main__':
    # Print MongoDB server information to check connection
    print(client.server_info())
    app.run(debug=True)
