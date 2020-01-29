from model import Base, Quote

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///quotes.db',connect_args={'check_same_thread': False})
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()




def add_quote(quote_value, hashtag, media, link,):
    quote = Quote(quote=quote_value, hashtag = hashtag, media=media, link= link)
    session.add(quote)
    session.commit()

def query_all():
    all_quotes = session.query(
      Quote).all()
    return all_quotes

def print_all():
    all_quotes = session.query(
      Quote).all()
    for i in all_quotes:
        print("quote: " , i.quote)
        print("hashtag: " , i.hashtag)
        print("media: " , i.media)
        print("link: " , i.link)
 
def get_quote(quote):
    return session.query(Quote).filter_by(quote=quote).first()


def delete_quote(quote):
   session.query(Quote).filter_by(
       quote=quote).delete()
   session.commit()

def del_all_quotes():
    session.query(Quote).delete()
    session.commit()






# def add_user(name,secret_word):
#     user = User(username=name)
#     user.hash_password(secret_word)
#     session.add(user)
#     session.commit()

# def get_user(username):
#     """Find the first user in the DB, by their username."""
#     return session.query(User).filter_by(username=username).first()


# def updt_food(new_food):
# 	user=session.query(User).filter_by(fav_food=new_food).first()
# 	user.fav_food(new_food)
# 	session.commit()

# def get_user_food(food):
# 	return session.query(User).filter_by(fav_food=food).first()

	
