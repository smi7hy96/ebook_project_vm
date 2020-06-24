from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
import random
from database.phsh import *

engine = create_engine('sqlite:///:memory:', connect_args={'check_same_thread': False})
metadata = MetaData()
conn = engine.connect()

users = Table('users', metadata,
              Column('user_id', Integer, primary_key=True),
              Column('name', String(20)),
              Column('email', String(30)),
              Column('phone_no', String(15)),
              Column('password', String())
              )
users = users
ebooks = Table('ebooks', metadata,
               Column('book_id', Integer, primary_key=True),
               Column('title', String),
               Column('author', String),
               Column('genre', String),
               Column('release_date', String),
               Column('image_source', String),
               Column('description', String),
               Column('user_id', None, ForeignKey('users.user_id'))
               )
ebooks = ebooks
booking = Table('booking', metadata,
                Column('booking_id', Integer, primary_key=True),
                Column('user_id', None, ForeignKey('users.user_id')),
                Column('book_id', None, ForeignKey('ebooks.book_id')),
                Column('date', String)
                )
booking = booking
metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def insert_ebook(title, author, genre, release_date, image_source, description, user_id=None):
    if user_id is None:
        user_id = 1
    ins = ebooks.insert().values(title=title, author=author, genre=genre, release_date=release_date,
                                      image_source=image_source, description=description, user_id=user_id)
    result = conn.execute(ins)
    return result.inserted_primary_key


def select_all_books():
    s = select([ebooks])
    result_list = []
    result = conn.execute(s)
    while True:
        row = result.fetchone()
        if row is None:
            break
        result_list.append(row)
    return result_list


def organise_list(result_list):
    id_list = []
    title_list = []
    author_list = []
    genre_list = []
    release_date_list = []
    image_source_list = []
    description_list = []
    return_list = []
    for value in result_list:
        title_list.append(value[1])
        author_list.append(value[2])
        genre_list.append(value[3])
        release_date_list.append(value[4])
        image_source_list.append(value[5])
        description_list.append(value[6])
        id_list.append(value[0])

    return_list.append(title_list)
    return_list.append(author_list)
    return_list.append(genre_list)
    return_list.append(release_date_list)
    return_list.append(image_source_list)
    return_list.append(description_list)
    return_list.append(id_list)
    return return_list


def select_all_separate():
    result_list = select_all_books()
    return_list = organise_list(result_list)
    return return_list


def select_six_random():
    result_list = select_all_books()
    num_list = []
    new_result_list = []
    if len(result_list) > 0:
        for x in range(6):
            repeat = False
            while not repeat:
                rand = random.randint(0, len(result_list) - 1)
                if rand not in num_list:
                    repeat = True
            num_list.append(rand)
            new_result_list.append(result_list[rand])
        return_list = organise_list(new_result_list)
        return return_list
    else:
        return []


def select_books_by_genre(genre):
    result_list = []
    s = select([ebooks]). \
        where(and_(ebooks.c.genre == genre))
    result = conn.execute(s)
    while True:
        row = result.fetchone()
        if row is None:
            break
        result_list.append(row)
    return result_list


def select_books_by_name(name):
    s = session.query(ebooks).\
        filter(ebooks.c.title.ilike('%{}%'.format(name))).all()
    return s


def get_by_name(name):
    result_list = select_books_by_name(name)
    return_list = organise_list(result_list)
    return return_list


def select_one_book(book_id):
    result_list = []
    s = select([ebooks]). \
        where(and_(ebooks.c.book_id == book_id))
    result = conn.execute(s)
    while True:
        row = result.fetchone()
        if row is None:
            break
        result_list.append(row)
    return result_list


def insert_user(name, email, phone_no, password):
        hsh_pass = hash_password(password)
        ins = users.insert().values(name=name, email=email, phone_no=phone_no, password=hsh_pass)
        result = conn.execute(ins)
        return result.inserted_primary_key


def log_in_user(user_id, password):
    result = select_one_user(user_id)
    if len(result) == 0:
        return False
    stored_pword = result[0][4]
    if verify_password(password, stored_pword):
        print("TRUE")
        return True
    else:
        print("FALSE")
        return False


def change_password_func(user_id, old_password, new_password):
    if log_in_user(user_id, old_password):
        hsh_pass = hash_password(new_password)
        s = users.update().values(password=hsh_pass).\
            where(users.c.user_id == user_id)
        conn.execute(s)
        return True
    else:
        return False


def select_one_user(user_id):
    result_list = []
    s = select([users]). \
        where(and_(users.c.user_id == user_id))
    result = conn.execute(s)
    while True:
        row = result.fetchone()
        if row is None:
            break
        result_list.append(row)
    return result_list

