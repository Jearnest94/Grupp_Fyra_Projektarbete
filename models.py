import datetime
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, current_user
from app import db, admin

message_recv = db.Table('message_recv',
                        db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                        db.Column('message_id', db.Integer, db.ForeignKey('message.message_id'), primary_key=True)
                        )


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(100))
    mangocount = db.Column(db.Integer, default=0)
    admin = db.Column(db.BOOLEAN, default=False)
    online = db.Column(db.BOOLEAN, default=False)
    public_RSA = db.Column(db.String(512))
    last_message_read_time = db.Column(db.DateTime)
    sent_messages = db.relationship('Message', backref='sender', lazy=True)
    recv_messages = db.relationship('Message', secondary=message_recv, lazy='subquery',
                                    backref=db.backref('recipients', lazy=True))

    def new_messages(self):
        data = db.session.query(Message, message_recv).join(Message).all()
        return


class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.admin


class Message(db.Model):
    message_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(50))
    content = db.Column(db.String(250))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    has_been_read = db.Column(db.BOOLEAN, default=False)
    encrypted_AES_key = db.Column(db.String(512))


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_server = db.Column(db.String(150))
    name_client = db.Column(db.String(150))
    ip_server = db.Column(db.String(100))
    notified = db.Column(db.BOOLEAN, default=False)


admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Message, db.session))
admin.add_view(MyModelView(Chat, db.session))