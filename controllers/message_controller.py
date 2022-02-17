from flask_login import current_user
from app import db
from controllers.user_controller import get_user_by_id
from models import Message, message_recv, Chat


def create_message(title, content, recipient_id, encrypted_AES_key):
    from models import Message
    user = current_user
    message = Message(title=title, content=content, sender_id=user.id, has_been_read=False,
                      encrypted_AES_key=encrypted_AES_key)
    recipient_id = int(recipient_id)
    recipient = get_user_by_id(recipient_id)
    message.recipients.append(recipient)
    from app import db
    db.session.add(message)
    db.session.commit()


def create_chat(name_server, name_client, ip_server):
    from models import Chat
    chat = Chat(name_server=name_server, name_client=name_client, ip_server=ip_server)
    from app import db
    db.session.add(chat)
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


def mark_as_notified():
    chat_data = db.session.query(Chat).all()
    notifications = []
    for chat in chat_data:
        if current_user.name == chat.name_client:
            notifications.append(chat.id)
    for chat_id in notifications:
        chat = Chat.query.filter_by(id=chat_id).first()
        chat.notified = 1
        db.session.commit()
