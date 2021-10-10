""" Model for GovFix app """

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class Subscriber(db.Model):
    """A subscriber"""

    __tablename__ = "subscribers"

    subscriber_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    full_name = db.Column(db.String(180), nullable=False)
    email = db.Column(db.String(180), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    industry = db.Column(db.String(50), nullable=False)
    use_case = db.Column(db.String(50), nullable=False)

class Bookmark(db.Model):

    __tablename__ = "bookmarks"

    article_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    author = db.Column(db.String(180), nullable=False)
    url = db.Column(db.Text, nullable=False)
    bookmark_date = db.Column(db.DateTime)
    subscriber_id = db.Column(db.Integer, db.ForeignKey(Subscriber.subscriber_id))

    subscriber = db.relationship("Subscriber", backref="bookmarks")




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