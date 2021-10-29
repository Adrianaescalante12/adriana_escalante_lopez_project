from flask import (Flask, render_template, request, flash, session, redirect, jsonify)
from model import connect_to_db
import json
import requests
from datetime import datetime, timedelta
import crud
import os
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

API_KEY = os.environ['NEWSAPI_KEY']

#today's date, turned to ISO 8601 format
td = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z')

#date 2 weeks ago (12 days ago)
two_weeks = datetime.now() -  timedelta(days = 12)

@app.route("/")
def homepage():
    """Homepage linking to jinja template with forms for sign in and subscriber sign up"""
    return render_template("homepage.html")

@app.route("/login", methods=["POST"])
def handle_login():
    email = request.form.get("email")
    password = request.form.get("password")
    # first check if email exist/subscriber exists
    if password == crud.subscriber_password(email):
        session["subscriber"] = email
        flash("Successful login")
        return redirect("/article-feed")
    else:
        flash("Email or password is incorrect")
        return redirect("/")

@app.route("/subscriber-sign-up", methods=["POST"])
def register_subscriber():
    """Create a new subscriber"""
    fullname = request.form.get('fullname')
    email = request.form.get('email')
    password = request.form.get('password')
    industry = request.form.get('industry')
    usecase = request.form.get('usecase')

    subscriber = crud.get_subscriber_by_email(email)
    print(subscriber)
    
    if subscriber:
        flash("There seems to be an account associated to this email already.")
        print("reached the if subscriber")
    else:
        crud.create_subscriber(fullname, email, password, industry, usecase)
        flash("Account created successfully. Try logging in.")
        print("reached the else create subscriber")
    
    return redirect("/")


@app.route("/article-feed")
def article_feed():
    """Connect to the NEWSAPI to get articles from past two weeks based on keywords and popularity"""

    url = f'https://newsapi.org/v2/everything'
    payload = {'language': 'en',
               'q': 'Department of Commerce OR Department of Education OR Department of Energy OR Department of Health and Human Services OR Department of Homeland Security OR Department of Housing and Urban Development OR Department of Justice OR Department of Labor OR Department of State OR Department of Transportation OR Department of Treasury OR Department of Veterans Affairs OR Executive Office of the President',
               'from': '{td}',
               'to': '{two_weeks}',
               'sortBy': 'popularity'}
    headers = {'X-Api-Key': API_KEY,
               'Accept': 'application/json',
               'Content-Type': 'application/json'}
    
    res = requests.get(url, params=payload, headers=headers)
    print(res)
   
    data = res.json()
    # print(data)
    articles = data['articles']
    article_data = [{'source':article['source']['name'], 'title':article['title'], 
                    'author':article['author'], 'description':article['description'],
                    'url':article['url']} for article in articles]
  
    # print(f"data as python: {articles}")
    
    subscribers_name = session.get("subscriber")

    return render_template("feed.html",article_data=article_data, subscribers_name=session.get("subscriber"))
   
    #left side what I call in jinja template, right side server object/variable

@app.route("/handle-bookmarks", methods=["POST"])
def handle_bookmarks():
    """Create a new bookmark"""
    source = request.json.get("source")
    title = request.json.get("title")
    author = request.json.get("author")
    description  = request.json.get("description")
    url  = request.json.get("url")
    bookmark_date = td
    subscriber_email = session.get("subscriber")
    subscriber_id = crud.subscriber_id(subscriber_email)


    crud.create_bookmark(source, title, author, description, url, bookmark_date, subscriber_id)
    flash("Successful Bookmark")

    #Use javascript to add that alert bc the point of using ajax is to not refresh

    return redirect("/article-feed")

    #call the crud function once you get the form inputs right

@app.route("/view-all-my-bookmarks")
def all_my_bookmarks():
    #use session
    subscriber_email = session.get("subscriber")
    print(subscriber_email)
    subscriber_id = crud.subscriber_id(subscriber_email)
    print(subscriber_id)
    bookmarks = crud.get_bookmarks_by_subscriber_id(subscriber_id)



    return render_template("all-bookmarks.html", bookmarks=bookmarks)




if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)