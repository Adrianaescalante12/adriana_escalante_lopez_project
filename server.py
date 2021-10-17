from flask import (Flask, render_template, request, flash, session, redirect)
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
    return render_template("homepage.html")

@app.route("/article-feed")
def article_feed():
    url = f'https://newsapi.org/v2/top-headline?apiKey={API_KEY}'
    payload = {'country': "us",
               'q': "Department of Defense",
               'pageSize': "50"}
    # head = {'Accept': "application/json",
    #         'Content-Type': "application/json"}
    
    res = requests.get(url, params=payload, headers=head)
    data = res.json()
    
    # source = data['_embedded']['articles']['source']
    # title = data['_embedded']['articles']['title']
    # author = data['_embedded']['articles']['author']
    # description = data['_embedded']['articles']['description']
    # url = data['_embedded']['articles']['url']
    
    print(f"data: {data}")
   
    # return render_template("feed.html",
    #                         source=source,
    #                         title=title,
    #                         author=author,
    #                         description=description,
    #                         url=url)

    #left side what I call in jinja template, right side server object/variable

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)