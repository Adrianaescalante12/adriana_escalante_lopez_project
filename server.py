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

#today's date, turned to ISO 8601 format for db
td = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z')

#date 2 weeks ago (12 days ago)
TWO_WEEKS = datetime.now() -  timedelta(days = 12)

#today's date for feed form
td2 = datetime.now().strftime('%Y-%m-%d')

#One month from today for feed form
ONE_MONTH = datetime.now() -  timedelta(days = 30)

@app.route("/")
def homepage():
    """Homepage linking to jinja template with forms for sign in and subscriber sign up"""
    return render_template("homepage.html")

@app.route("/login", methods=["POST"])
def handle_login():
    """Log in users who's password matches their email"""
    email = request.form.get("email")
    password = request.form.get("password")
    
    if not crud.subscriber_password(email):
        flash("No account exists with this email")
        return redirect("/")
    else:
        if password == crud.subscriber_password(email):
            session["subscriber"] = email
            flash("Successful login")
            return redirect("/article-feed")
        else:
            flash("Email or password is incorrect")
            return redirect("/")

@app.route("/logout")
def handle_logout():
    """Send user back to homepage and have them re log in if signed out (logic in article feed forces them to resign in)"""

    if "subscriber" in session:
        session.clear()
        return redirect("/")

@app.route( "/subscriber-sign-up", methods=["POST"])
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
        # print("reached the if subscriber")
    else:
        crud.create_subscriber(fullname, email, password, industry, usecase)
        flash("Account created successfully. Try logging in.")
        # print("reached the else create subscriber")
    
    return redirect("/")


@app.route("/article-feed")
def article_feed():
    """Connect to the NEWSAPI to get articles from past two weeks based on keywords and popularity"""
    #Do not allow users not logged in to enter this page
    subscriber = session.get("subscriber")
    if subscriber is  None:
        return redirect("/")
    
    url = f'https://newsapi.org/v2/everything'
    payload = {'language': 'en',
            'q': f'Department of Commerce OR Department of Education OR Department of Energy OR Department of Defense OR Department of Homeland Security OR Department of Housing and Urban Development OR Department of Justice OR Department of Labor OR Department of State',
            'from': f'{td}',
            'to': f'{TWO_WEEKS}',
            'sortBy': 'popularity'}
    headers = {'X-Api-Key': API_KEY,
            'Accept': 'application/json',
            'Content-Type': 'application/json'}
    
    res = requests.get(url, params=payload, headers=headers)
    # print(res.__dict__)
    # print()
    

    data = res.json()
    # print(data)
    articles = data['articles']
    article_data = [{'source':article['source']['name'], 'title':article['title'], 
                    'author':article['author'], 'description':article['description'],
                    'url':article['url']} for article in articles]

    
    
    email = session.get("subscriber")
    subscriber_name = crud.subscriber_name(email)
    return render_template("feed.html",article_data=article_data, subscribers_name=subscriber_name, TWO_WEEKS=TWO_WEEKS, td=td, td2=td2, ONE_MONTH=ONE_MONTH)
    #left side what I call in jinja template, right side server object/variable
    

@app.route("/article-feed", methods=["POST"])
def article_feed2():
    """CUSTOMIZED request to NEWSAPI to get articles from past two weeks based on user keyword search"""
    keywordsearch = request.form.get("keywordsearch")
    start = request.form.get("articlefeed-from")
    # print(start)
    end = request.form.get("articlefeed-to")
    # print(TWO_WEEKS)
    # print(end)


    url = f'https://newsapi.org/v2/everything'
    payload = {'language': 'en',
                'q': 'Department of Commerce OR Department of Education OR Department of Energy OR Department of Defense OR Department of Homeland Security OR Department of Housing and Urban Development OR Department of Justice OR Department of Labor OR Department of State',
               'from': f'{start}',
               'to': f'{end}',
               'sortBy': 'popularity'}
    if keywordsearch:
        payload['q'] = keywordsearch

    
    headers = {'X-Api-Key': API_KEY,
               'Accept': 'application/json',
               'Content-Type': 'application/json'}
    
    res = requests.get(url, params=payload, headers=headers)
    # print(res)
    # print(f"********************{keywordsearch}")
   
    data = res.json()
    print(data)
    articles = data['articles']
    print(articles)
    article_data = [{'source':article['source']['name'], 'title':article['title'], 
                    'author':article['author'], 'description':article['description'],
                    'url':article['url']} for article in articles]
  
    
    email = session.get("subscriber")
    subscriber_name = crud.subscriber_name(email)
    
    return render_template("feed.html", article_data=article_data, subscribers_name=subscriber_name, td2=td2, TWO_WEEKS=TWO_WEEKS, start=start, end=end, ONE_MONTH=ONE_MONTH)


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
    
    bookmark_urls = crud.get_bookmark_urls_by_subscriber_id(subscriber_id)
    
    if url not in bookmark_urls:
        bookmark = crud.create_bookmark(source, title, author, description, url, bookmark_date, subscriber_id)
        return jsonify({"data":bookmark.title, "status":200, "message":"Bookmark Added"})
    else: 
        return jsonify({"data":title, "status":500, "message":"Bookmark already exists"})
    #FIX THIS ELSE!

@app.route("/view-all-my-bookmarks")
def all_my_bookmarks():
    """View all bookmarks for subscriber logged in"""
    #use session
    subscriber_email = session.get("subscriber")
    subscriber_id = crud.subscriber_id(subscriber_email)
    bookmarks = crud.get_bookmarks_by_subscriber_id(subscriber_id)
    
    return render_template("all-bookmarks.html", bookmarks=bookmarks)

@app.route("/handle-unbookmark", methods=["POST"])
def handle_unbookmark():
    """Unbookmark an article"""
    url  = request.json.get("url")
    subscriber_email = session.get("subscriber")
    subscriber_id = crud.subscriber_id(subscriber_email)

    unbookmark = crud.unbookmark(url, subscriber_id)
    

    return jsonify({"status":200, "message":"Unbookmark Successful"})



if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)