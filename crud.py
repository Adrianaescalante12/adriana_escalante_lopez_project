from model import db, Subscriber, Bookmark, connect_to_db

def create_subscriber(full_name, email, password, industry, use_case):
    #
    subscriber =  Subscriber(full_name=fullname,
                            email=email,
                            password=password, 
                            industry=industry, 
                            use_case=usecase)

    db.session.add(subscriber)
    db.session.commit()

    return subscriber

def create_bookmark(source, title, author, description, url, bookmark_date, subscriber):
    bookmark = Bookmark(source=source, 
                        title=title, 
                        author=author, 
                        description=description, 
                        url=url, 
                        bookmark_date=bookmarkdate,     
                        subscriber=subscriber)

    db.session.add(bookmark)
    db.session.commit()

    return bookmark

def get_subscriber_by_email(email):
    return Subscriber.query.get(email)


if __name__ == '__main__':
    from server import app
    connect_to_db(app)