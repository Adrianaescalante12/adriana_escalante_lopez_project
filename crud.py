from model import db, Subscriber, Bookmark, connect_to_db

def create_subscriber(fullname, email, password, industry, usecase):
    #
    subscriber =  Subscriber(full_name=fullname,
                            email=email,
                            password=password, 
                            industry=industry, 
                            use_case=usecase)

    db.session.add(subscriber)
    db.session.commit()

    return subscriber

def create_bookmark(source, title, author, description, url, bookmark_date, subscriber_id):
    bookmark = Bookmark(source=source, 
                        title=title, 
                        author=author, 
                        description=description, 
                        url=url, 
                        bookmark_date=bookmark_date,     
                        subscriber_id=subscriber_id)

    db.session.add(bookmark)
    db.session.commit()

    return bookmark

def get_subscriber_by_email(email):
    return Subscriber.query.filter(Subscriber.email == email).first()

def subscriber_id(email):
    subscriber = Subscriber.query.filter(Subscriber.email == email).first()
    subscriber_id = subscriber.subscriber_id

    return subscriber_id

def subscriber_password(email):
    subscriber = Subscriber.query.filter(Subscriber.email == email).first()
    
    if subscriber is not None:
        return subscriber.password
    else:
        return None

def get_bookmarks_by_subscriber_id(subscriber_id):
    bookmarks = Bookmark.query.filter_by(subscriber_id=subscriber_id).all()

    return bookmarks

def unbookmark(url, subscriber_id):
    
    bookmark = Bookmark.query.filter((Bookmark.url==url)&(Bookmark.subscriber_id==subscriber_id)).delete()
    print(bookmark)

    db.session.commit()

    return bookmark
    





if __name__ == '__main__':
    from server import app
    connect_to_db(app)