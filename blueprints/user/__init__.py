from flask import Blueprint, render_template

bp_user = Blueprint('bp_user', __name__)


@bp_user.get('/profile')
def profile_get():
    return render_template("profile.html")


@bp_user.get('/chat')
def chat_get():
    return render_template('chat.html')


@bp_user.get('/messages')
def messages_get():
    return render_template('messages.html')
