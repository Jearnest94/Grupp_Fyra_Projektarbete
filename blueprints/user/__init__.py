from flask import Blueprint, render_template, session, redirect, url_for
from flask_login import current_user
from models import User

bp_user = Blueprint('bp_user', __name__)


@bp_user.get('/profile')
def profile_get():
    return render_template("profile.html", name=current_user.name)


@bp_user.get('/chat')
def chat_get():
    return render_template('chat.html', name=current_user.name)


@bp_user.get('/messages')
def messages_get():
    return render_template('messages.html', name=current_user.name)


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
