""" Model for GovFix app """

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class Subscriber(db.Model):
    """A subsscriber"""

    __tablename__ = "subscribers"

    subscriber_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    full_name = db.Column(db.String(180))
    email = db.Column(db.String(180), unique=True)
    password = db.Column(db.String(50))
    industry = db.Column(db.String(50))
    use_case = db.Column(db.String(50))

class Bookmark(db.Model):

    __tablename__ = "bookmarks"

    article_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(250))
    author = db.Column(db.String(180))
    url = db.Column(db.Text)
    bookmark_date = db.Column(db.DateTime)
    subscriber_id = db.Column(db.Integer, db.ForeignKey(subscriber.subscriber_id))

    subscriber = db.relationship("Subscriber", backref="govfix")




def connect_to_db(flask_app, db_uri="postgresql:///govfix", echo=False):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app
    connect_to_db(app)