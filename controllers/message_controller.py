from flask_login import current_user

from controllers.user_controller import get_user_by_id


def create_message(title, content, recipient_id):
    from models import Message
    user = current_user
    message = Message(title=title, content=content, sender_id=user.id)
    recipient_id = int(recipient_id)
    recipient = get_user_by_id(recipient_id)
    message.recipients.append(recipient)
    from app import db
    db.session.add(message)
    db.session.commit()


def get_user_messages():
    return current_user.recv_messages
