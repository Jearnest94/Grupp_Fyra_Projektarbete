import re
from datetime import datetime

from flask import Blueprint, render_template, session, request, redirect, url_for
from flask_login import current_user, login_required, logout_user

import mqtt_publish
from app import db
from controllers.message_controller import get_user_messages, create_message, mark_as_read
from controllers.user_controller import get_all_users, get_user_by_id
from models import User, Message, message_recv

bp_user = Blueprint('bp_user', __name__)


@bp_user.get('/')
def index():
    users = get_all_users()
    messages = get_user_messages()
    messages_data = db.session.query(Message.has_been_read, message_recv).join(Message).all()
    return render_template("index.html", name=current_user.name, userlist=users,
                           mangocount=User.query.filter_by(email=current_user.email).first().mangocount, messages=messages, messages_data=messages_data)


@bp_user.post('/')
def mangocount_post():
    email = session['email']
    user = User.query.filter_by(email=email).first()
    if user.mangocount is None:
        user.mangocount = 1
    else:
        user.mangocount += 1
    db.session.commit()
    return render_template('index.html', mangocount=str(user.mangocount))


@bp_user.get('/inbox')
def inbox_get():
    messages = get_user_messages()
    messages_data = db.session.query(Message.has_been_read, message_recv).join(Message).all()
    mark_as_read()
    return render_template("inbox.html", email=current_user.email, messages=messages, messages_data=messages_data)


@bp_user.get('/chat')
def chat_get():
    users = get_all_users()
    messages_data = db.session.query(Message.has_been_read, message_recv).join(Message).all()
    return render_template('chat.html', name=current_user.name, userlist=users, messages_data=messages_data)

@bp_user.get('/chat2')
def chat2_get():

    return render_template('chat2.html', name=current_user.name)


@bp_user.get('/profile')
def profile_get():
    users = get_all_users()
    messages_data = db.session.query(Message.has_been_read, message_recv).join(Message).all()
    return render_template("profile.html", userlist=users, name=current_user.name, email=current_user.email,
                           mangocount=User.query.filter_by(email=current_user.email).first().mangocount, messages_data=messages_data)


@bp_user.post('/profile')
def profile_post():
    email = session['email']
    user = User.query.filter_by(email=email).first()
    user.public_RSA = request.form['generated_RSA_public']
    public_key = re.sub("\n", "", user.public_RSA)
    db.session.commit()
    with open(f'./chat/rsa_keys/{current_user.name.lower()}_public.pem', 'w') as out_file:
        out_file.write(public_key)
    return redirect(url_for('bp_user.profile_get'))


@bp_user.get('/profile/<user_id>')
def profile_get_user(user_id):
    user_id = int(user_id)
    recipient = get_user_by_id(user_id)
    messages_data = db.session.query(Message.has_been_read, message_recv).join(Message).all()
    return render_template('profile_user.html', recipent=recipient, messages_data=messages_data)


@bp_user.get('/messages/<user_id>')
def messages_get_user(user_id):
    user_id = int(user_id)
    recipient = get_user_by_id(user_id)
    messages_data = db.session.query(Message.has_been_read, message_recv).join(Message).all()
    return render_template('messages.html', name=current_user.name, email=current_user.email, recipient=recipient, messages_data=messages_data)


@bp_user.post('/messages/<user_id>')
def messages_post(user_id):
    title = request.form['title']
    content = request.form['content']
    encrypted_AES_key = request.form['encrypted_AES_key']
    user_id = int(user_id)
    create_message(title, content, user_id, encrypted_AES_key)
    mqtt_publish.publish(user_id, current_user.email)
    return redirect(url_for('bp_user.messages_get_sent'))


@bp_user.get('/messages/sent')
def messages_get_sent():
    messages_data = db.session.query(Message.has_been_read, message_recv).join(Message).all()
    return render_template('message_sent.html', messages_data=messages_data)


@bp_user.get('/logout')
@login_required
def logout():
    user = current_user
    user.online = False

    from app import db
    db.session.commit()
    logout_user()
    return redirect(url_for('bp_open.index'))
