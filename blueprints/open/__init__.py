from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_user
from app import db
from models import User, Message, message_recv, Chat
from werkzeug.security import generate_password_hash, check_password_hash

bp_open = Blueprint('bp_open', __name__)


@bp_open.get('/')
def index():
    chat_data = db.session.query(Chat).all()
    messages_data = db.session.query(Message.has_been_read, message_recv).join(Message).all()
    return render_template("index.html", messages_data=messages_data, chat_data=chat_data)


@bp_open.get('/login')
def login_get():
    return render_template('login.html')


@bp_open.post('/login')
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    session['email'] = email
    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('bp_open.login_get'))  # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)

    login_user(user)
    user.online = True

    from app import db
    db.session.commit()

    return redirect(url_for('bp_user.profile_get'))


@bp_open.get('/signup')
def signup_get():
    return render_template('signup.html')


@bp_open.post('/signup')
def signup_post():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    hashed_password = generate_password_hash(password, method='sha256')

    user = User.query.filter_by(email=email).first()
    if user:
        flash("Email already in use.")
        return redirect(url_for('bp_open.signup_get'))

    new_user = User(name=name, email=email, password=hashed_password)

    from app import db
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('bp_open.login_get'))
