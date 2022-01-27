from flask import Blueprint, render_template, session, request, redirect, url_for
from flask_login import current_user, login_required, logout_user
from controllers.message_controller import get_user_messages, create_message
from controllers.user_controller import get_all_users, get_user_by_id
from models import User, Message

bp_user = Blueprint('bp_user', __name__)


@bp_user.get('/')
def index():
    users = get_all_users()
    return render_template("index.html", name=current_user.name, userlist=users,
                           mangocount=User.query.filter_by(email=current_user.email).first().mangocount)


@bp_user.post('/')
def mangocount_post():
    from app import db
    email = session['email']
    user = User.query.filter_by(email=email).first()
    if user.mangocount is None:
        user.mangocount = 1
    else:
        user.mangocount += 1
    print(user.mangocount)
    db.session.commit()
    return render_template('index.html', mangocount=str(user.mangocount))


@bp_user.get('/inbox')
def inbox_get():
    messages = get_user_messages()
    return render_template("inbox.html", email=current_user.email, messages=messages)


@bp_user.get('/chat')
def chat_get():
    users = get_all_users()
    return render_template('chat.html', name=current_user.name, userlist=users)


@bp_user.get('/profile')
def profile_get():
    users = get_all_users()
    return render_template("profile.html", userlist=users, name=current_user.name, email=current_user.email,
                           mangocount=User.query.filter_by(email=current_user.email).first().mangocount)


@bp_user.get('/profile/<user_id>')
def profile_get_user(user_id):
    user_id = int(user_id)
    recipient = get_user_by_id(user_id)
    return render_template('profile_user.html',  recipent=recipient)


@bp_user.get('/messages/<user_id>')
def messages_get_user(user_id):
    user_id = int(user_id)
    recipient = get_user_by_id(user_id)
    return render_template('messages.html', name=current_user.name, email=current_user.email, recipient=recipient)


@bp_user.post('/messages/<user_id>')
def messages_post(user_id):
    title = request.form['title']
    content = request.form['content']
    user_id = int(user_id)
    print(user_id)
    recipient = get_user_by_id(user_id)
    print(recipient)
    create_message(title, content, user_id)
    return redirect(url_for('bp_user.messages_get_sent'))


@bp_user.get('/messages/sent')
def messages_get_sent():
    return render_template('message_sent.html')


# @bp_user.get('/messages_recipient')
# def messages_recipient_get():
#     return render_template('messages.html', name=current_user.name, email=current_user.email)


# @bp_user.post('/messages')
# def messages_post():
#     title = request.form['title']
#     content = request.form['content']
#     email = request.form['recipient']
#     recipient_id = User.query.filter_by(email=email).first().id
#     create_message(title, content, recipient_id)
#     return redirect(url_for('bp_user.messages_get'))


@bp_user.get('/logout')
@login_required
def logout():
    user = current_user
    user.online = False

    from app import db
    db.session.commit()
    logout_user()
    return redirect(url_for('bp_open.index'))
