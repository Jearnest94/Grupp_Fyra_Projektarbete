import re
from flask import Blueprint, render_template, session, request, redirect, url_for
from flask_login import current_user, login_required, logout_user
import mqtt_publish
from app import db
from controllers.message_controller import get_user_messages, create_message, mark_as_read, \
    create_chat, mark_as_notified
from controllers.user_controller import get_all_users, get_user_by_id, get_user_server_ip
from models import User, Message, message_recv, Chat

bp_user = Blueprint('bp_user', __name__)


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


@bp_user.get('/profile')
def profile_get():
    users = get_all_users()
    chat_data = db.session.query(Chat).all()
    messages_data = db.session.query(Message.has_been_read, message_recv).join(Message).all()
    return render_template("profile.html", userlist=users, name=current_user.name, email=current_user.email,
                           mangocount=User.query.filter_by(email=current_user.email).first().mangocount,
                           messages_data=messages_data, chat_data=chat_data)


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
    chat_data = db.session.query(Chat).all()
    name_client = get_user_by_id(user_id)
    ip_server = get_user_server_ip()
    messages_data = db.session.query(Message.has_been_read, message_recv).join(Message).all()
    return render_template('profile_user.html', recipient=recipient, messages_data=messages_data,
                           name_client=name_client,
                           ip_server=ip_server, chat_data=chat_data)


@bp_user.get('/inbox')
def inbox_get():
    messages = get_user_messages()
    chat_data = db.session.query(Chat).all()
    messages_data = db.session.query(Message.has_been_read, message_recv).join(Message).all()
    mark_as_read()
    return render_template("inbox.html", email=current_user.email, messages=messages, messages_data=messages_data,
                           chat_data=chat_data)


@bp_user.get('/chat_requests')
def chat_requests_get():
    chat_data = db.session.query(Chat).all()
    return render_template('chat_requests.html', chat_data=chat_data)


@bp_user.get('/chat_confirm')
def chat_confirm():
    mark_as_notified()
    return redirect(url_for('bp_open.index'))


@bp_user.post('/chat/<user_id>')
def chat_post(user_id):
    user_id = int(user_id)
    name_client = get_user_by_id(user_id)
    name_server = current_user.name
    ip_server = get_user_server_ip()
    create_chat(name_server, name_client.name, ip_server)
    return redirect(url_for('bp_open.index'))


@bp_user.get('/messages/<user_id>')
def messages_get_user(user_id):
    user_id = int(user_id)
    recipient = get_user_by_id(user_id)
    messages_data = db.session.query(Message.has_been_read, message_recv).join(Message).all()
    return render_template('messages.html', name=current_user.name, email=current_user.email, recipient=recipient,
                           messages_data=messages_data)


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
    chat_data = db.session.query(Chat).all()
    messages_data = db.session.query(Message.has_been_read, message_recv).join(Message).all()
    return render_template('message_sent.html', messages_data=messages_data, chat_data=chat_data)


@bp_user.get('/logout')
@login_required
def logout():
    user = current_user
    user.online = False
    from app import db
    db.session.commit()
    logout_user()
    return redirect(url_for('bp_open.index'))