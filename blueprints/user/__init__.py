from flask import Blueprint, render_template, session, request, redirect, url_for
from flask_login import current_user, login_required
from models import User, Message

bp_user = Blueprint('bp_user', __name__)


@bp_user.get('/')
def index():
    return render_template("index.html", name=current_user.name,
                           mangocount=User.query.filter_by(email=current_user.email).first().mangocount)


@bp_user.post('/')
def mangocount_post():
    from app import db
    email = session['email']
    user = User.query.filter_by(email=email).first()
    if user.mangocount == None:
        user.mangocount = 1
    else:
        user.mangocount += 1
    print(user.mangocount)
    db.session.commit()
    return render_template('index.html', mangocount=str(user.mangocount))


@bp_user.get('/profile')
def profile_get():
    return render_template("profile.html", name=current_user.name, email=current_user.email,
                           mangocount=User.query.filter_by(email=current_user.email).first().mangocount)


@bp_user.get('/chat')
def chat_get():
    return render_template('chat.html', name=current_user.name)


@bp_user.get('/messages')
def messages_get():
    return render_template('messages.html', name=current_user.name, email=current_user.email)


@bp_user.post('/messages')
def messages_post():
    print('msg_post')
    touser = request.form.get('touser')
    title = request.form.get('title')
    content = request.form.get('content')
    fromuser = current_user.email
    new_message = Message(touser=touser, title=title, content=content, fromuser=fromuser)
    from app import db
    db.session.add(new_message)
    db.session.commit()

    return redirect(url_for('bp_user.messages_get'))
