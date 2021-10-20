from flask import (Flask, render_template, request, flash, session, redirect, jsonify)
from model import connect_to_db
import json
import requests
# import crud
import os
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

API_KEY = os.environ['NEWSAPI_KEY']

@app.route("/")
def homepage():
    """Homepage linking to jinja template with forms for sign in and subscriber sign up"""
    return render_template("homepage.html")

@app.route("/article-feed")
def article_feed():
    """Connect to the API"""
    # url = f'https://newsapi.org/v2/top-headline?apiKey={API_KEY}'
    url = f'https://newsapi.org/v2/everything'
    payload = {'language': 'en',
               'q': 'Department of Commerce OR Department of Education OR Department of Energy OR Department of Health and Human Services OR Department of Homeland Security OR Department of Housing and Urban Development OR Department of Justice OR Department of Labor OR Department of State OR Department of Transportation OR Department of Treasury OR Department of Veterans Affairs OR Executive Office of the President'}
    headers = {'X-Api-Key': API_KEY,
               'Accept': 'application/json',
               'Content-Type': 'application/json'}
    
    res = requests.get(url, params=payload, headers=headers)
   
    data = res.json()
    articles = data['articles']
    article_data = [{'source':article['source']['name'], 'title':article['title'], 'author':article['author'], 'description':article['description'],'url':article['url']} for article in articles]
  
    # print(f"data as python: {articles}")
   
    return render_template("feed.html",article_data=article_data)
   
    #left side what I call in jinja template, right side server object/variable

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)