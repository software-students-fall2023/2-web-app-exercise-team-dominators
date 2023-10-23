from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
# from faker import Faker
import random
import logging
from datetime import datetime
from bson import ObjectId
from bson import json_util
import json


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
        # user = json.loads(json_util.dumps(userraw))

        if user:
            session["logged_in"] = True
            session["id"] = str(user.get("_id"))
            session["notifications"] = str(user.get("notifications"))
            return redirect(url_for("home"))
        else:
            return redirect(url_for("login_failed"))

    return render_template("login.html")

@app.route("/login_failed", methods=["GET", "POST"])
def login_failed():
    return render_template("login_failed.html")

#TODO: add signup page

@app.route('/home', methods=["GET"])
@app.route('/', methods=["GET"])
def home():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    featured_events = events.find().limit(20)



    return render_template("home.html", featured_events=featured_events)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    query = ""
    if request.method == 'POST':
        query = request.form.get('query')
        if query:
            search_results = events.find({"event_name": {"$regex": query, "$options": 'i'}})
        else:
            search_results = events.find()
    else:
        search_results = events.find()

    return render_template('search.html', events=search_results, query=query)


@app.route('/watchlist')
def watchlist():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    id = str(session.get("id"))

    print(id)

    watchlist = users.find_one({"_id": ObjectId(id)}).get("watchlist")
    watchlisted_events = []
    if watchlist is None:
        watchlisted_events = ["No events in watchlist"]
    else:
        for event in watchlist:
            result = events.find_one({"_id": ObjectId(event)})
            if result:
                watchlisted_events.append(result)
    return render_template('watchlist.html', events=watchlisted_events)

@app.route('/watchlist_edit', methods=['POST'])
def watchlist_edit():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    id = session.get("id")

    watchlist = users.find_one({"_id": ObjectId(id)}).get("watchlist")
    watchlisted_events = []
    if watchlist is None:
        watchlisted_events = ["No events in watchlist"]
    else:
        for event in watchlist:
            result = events.find_one({"_id": ObjectId(event)})
            if result:
                watchlisted_events.append(result)
    return render_template('watchlist_edit.html', events=watchlisted_events)

@app.route('/delete', methods=['POST'])
def delete():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    event_id = request.form.get('event_id')
    if event_id:
        users.update_one({"_id": ObjectId(session.get("id"))}, {"$pull": {"watchlist": ObjectId(event_id)}})
        return redirect(url_for('watchlist'))
    else:
        return "Error deleting from watchlist", 400

@app.route('/delete_all', methods=['POST'])
def delete_all():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    users.update_one({"_id": ObjectId(session.get("id"))}, {"$set": {"watchlist": []}})
    return redirect(url_for('watchlist'))

@app.route('/settings', methods=['GET'])
def settings():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    return render_template('settings.html')


@app.route('/settings_save', methods=['POST'])
def settings_save():
    # Access form data
    email = request.form.get('email')
    password = request.form.get('password')
    phone = request.form.get('phone')
    notify_email = True if request.form.get('notify_email') else False
    notify_phone = True if request.form.get('notify_phone') else False
    notify_app = True if request.form.get('notify_app') else False
    notification_mode = request.form.get('notification')
    #contact_us_message = request.form.get('contact_us')

    # Debugging: print form data to the console
    print(f"Email: {email}")
    print(f"Password: {password}")
    print(f"Phone: {phone}")
    print(f"Notify Email: {notify_email}")
    print(f"Notify Phone: {notify_phone}")
    print(f"Notify App: {notify_app}")
    print(f"Notification Mode: {notification}")
   

    # Update user's data in the database using the form data

    # Assuming you are storing the logged-in user's ID in the session
    user_id = session.get('id')

    if not user_id:
        # Handle the error where there's no user ID in the session.
        # Maybe redirect them to the login page?
        return redirect(url_for('login'))

    updates = {}

    if email:
        updates["email"] = email
    if password:
        updates["password_hash"] = password
    if phone:
        updates["phone"] = phone
    if notification_mode:
        updates["notification_mode"] = notification_mode

    # Update the notifications array
    updates["notifications"] = []
    if notify_email:
        updates["notifications"].append("email")
    if notify_phone:
        updates["notifications"].append("phone")
    if notify_app:
        updates["notifications"].append("app")

    # Update the database
    db.USer.update_one({"_id": ObjectId(user_id)}, {"$set": updates})

    return redirect(url_for('settings'))


@app.route('/event/<event_id>, methods=["GET"]')
def event_page(event_id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    event = events.find_one({"_id": ObjectId(event_id)})
    if event:
        return render_template('event.html', event=event)
    else:
        return "Event not found", 404

@app.route('/add_to_watchlist', methods=['POST'])
def add_to_watchlist():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    event_id = request.form.get('event_id')

    # TODO: update database
    price_drop = request.form.get('price')
    inventory_drop = request.form.get('inventory')
    restock_to = request.form.get('restock')


    if event_id:
        if users.find_one({"_id": ObjectId(session.get("id")), "watchlist": ObjectId(event_id)}):
            return redirect(url_for('watchlist'))
        else:
            users.update_one({"_id": ObjectId(session.get("id"))}, {"$push": {"watchlist": ObjectId(event_id)}})
        return redirect(url_for('watchlist'))
    else:
        return "Error adding to watchlist", 400

@app.route('/notification', methods=["GET"])
def notification():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    id = session.get("id")

    messages = users.find_one({"_id": ObjectId(id)}).get("notifications")

    if messages == []:
        messages.append("No messages")
    print(messages)

    return render_template("notification.html", messages = messages)

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))


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
    # print(client.server_info())
    app.run(debug=True)
