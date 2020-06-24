from flask import Flask, render_template, request, redirect, url_for
from database.database_full_connection import *
from database.example_books import *
from database.user_example import *
app = Flask(__name__)
current_user_id = 0
name = ''

@app.route("/")
def home():
    result_list = select_six_random()
    titles = result_list[0]
    authors = result_list[1]
    genres = result_list[2]
    release_dates = result_list[3]
    image_sources = result_list[4]
    descriptions = result_list[5]
    book_ids = result_list[6]
    return render_template("flip_card.html", titles=titles, authors=authors, genres=genres, release_dates=release_dates,
                           image_sources=image_sources, descriptions=descriptions, book_ids=book_ids, user_id=current_user_id, name=name)

@app.route("/all-books")
def all_books():
    result_list = select_all_separate()
    titles = result_list[0]
    authors = result_list[1]
    genres = result_list[2]
    release_dates = result_list[3]
    image_sources = result_list[4]
    descriptions = result_list[5]
    book_ids = result_list[6]
    return render_template("all_books.html", titles=titles, authors=authors, genres=genres, release_dates=release_dates, image_sources=image_sources, descriptions=descriptions, book_ids=book_ids, user_id=current_user_id, name=name)


@app.route("/book_id/<int:id>")
def book_id(id):
    new_list = []
    result_list = select_one_book(id)  # will retrieve different data depending on id
    ## example query
    for result in result_list:
        for value in result:
            new_list.append(value)
    title = new_list[1]
    author = new_list[2]
    genre = new_list[3]
    release_date = new_list[4]
    image_source = new_list[5]
    description = new_list[6]
    return render_template("book_template.html", title=title, author=author, genre=genre, release_date=release_date, image_source=image_source, description=description, user_id=current_user_id, name=name)


@app.route("/search_book")
def search_book():
    query = request.args['search']
    result_list = get_by_name(query)
    titles = result_list[0]
    authors = result_list[1]
    genres = result_list[2]
    release_dates = result_list[3]
    image_sources = result_list[4]
    descriptions = result_list[5]
    return render_template("search_book.html", titles=titles, authors=authors, genres=genres, release_dates=release_dates,
                           image_sources=image_sources, descriptions=descriptions, query=query, user_id=current_user_id, name=name)


@app.route("/about_us")
def about_us():
    return render_template("about_us.html", user_id=current_user_id, name=name)


# Add new book page methods - untested until page templates created.
@app.route("/add_book")
def add_book():
    return render_template("add_book.html", user_id=current_user_id, name=name)

@app.route("/add_new_book")
def add_new_book():
    title = request.args['title']
    author = request.args['author']
    genre = request.args['genre']
    release_date = request.args['release_date']
    image_source = request.args['image_source']
    description = request.args['description']
    return_num = insert_ebook(title, author, genre, release_date, image_source, description)
    return render_template("book_template.html", title=title, author=author, genre=genre, release_date=release_date, image_source=image_source, description=description, user_id=current_user_id, name=name)


@app.route("/go_to_login")
def go_to_login(attempt=None):
    if current_user_id == 0:
        return render_template("log-in.html", attempt=attempt, user_id=current_user_id, name=name)
    else:
        return redirect(url_for('home'))


@app.route("/log_in", methods=['POST'])
def log_in():
    user_id = request.form.get('user_id')
    password = request.form.get('password')
    global current_user_id
    if current_user_id == 0:
        if log_in_user(user_id, password):
            current_user_id = user_id
            new_list = []
            result_list = select_one_user(user_id)
            for result in result_list:
                for value in result:
                    new_list.append(value)
            global name
            name = new_list[1]
            print(name)
            return redirect(url_for('home'))
        else:
            return redirect(url_for('go_to_login'))
    else:
        return redirect(url_for('home'))


@app.route("/logout")
def logout():
    global current_user_id
    global name
    current_user_id = 0
    name = ''
    return redirect(url_for('home'))


@app.route("/change_password")
def change_password():
    if current_user_id != 0:
        return render_template("change_password.html", user_id=current_user_id, name=name)
    else:
        return redirect(url_for("go_to_login"))


@app.route("/change_password_complete", methods=['POST'])
def change_password_complete():
    old_password = request.form.get('old_pword')
    new_password = request.form.get('new_password')
    global current_user_id
    if log_in_user(current_user_id, old_password):
        change_password_func(current_user_id, old_password, new_password)
        return redirect(url_for('home'))
    else:
        return redirect(url_for('change_password'))


@app.route("/sign_up")
def sign_up():
    return render_template("sign-up.html", user_id=current_user_id, name=name)


@app.route("/sign_up_complete")
def sign_up_complete():
    user_name = request.args['name']
    email = request.args['email']
    phone_no = request.args['phone_no']
    password = request.args['password']
    return_num = insert_user(user_name, email, phone_no, password)
    print(return_num)
    global current_user_id
    global name
    current_user_id = return_num
    name = user_name
    return redirect(url_for('home'))


@app.route("/view_account_details")
def view_account_details():
    global current_user_id
    new_list = []
    if current_user_id != 0:
        result_list = select_one_user(current_user_id)
        for result in result_list:
            for value in result:
                new_list.append(value)
        a_user_id = new_list[0]
        user_name = new_list[1]
        email = new_list[2]
        phone_no = new_list[3]
        return render_template("view_account_details.html", a_user_id=a_user_id, user_name=user_name, email=email, phone_no=phone_no, user_id=current_user_id, name=name)
    else:
        return redirect(url_for("go_to_login"))


if __name__ == "__main__":
    app.run(debug=True)
