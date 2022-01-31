from flask_login import current_user

from app import db
from controllers.user_controller import get_user_by_id
from models import Message, message_recv


def create_message(title, content, recipient_id):
    from models import Message
    user = current_user
    message = Message(title=title, content=content, sender_id=user.id, has_been_read=False)
    recipient_id = int(recipient_id)
    recipient = get_user_by_id(recipient_id)
    message.recipients.append(recipient)
    from app import db
    db.session.add(message)
    db.session.commit()


def get_user_messages():
    return current_user.recv_messages


def mark_as_read():
    messages_data = db.session.query(Message.has_been_read, message_recv).join(Message).all()
    user_messages = []
    for message in messages_data:
        if current_user.id == message.user_id:
            user_messages.append(message.message_id)
    for message_id in user_messages:
        message = Message.query.filter_by(message_id=message_id).first()
        message.has_been_read = 1
        db.session.commit()
