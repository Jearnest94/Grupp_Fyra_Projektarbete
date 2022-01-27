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

    sent_messages = db.relationship('Message', backref='sender', lazy=True)
    recv_messages = db.relationship('Message', secondary=message_recv, lazy='subquery',
                                    backref=db.backref('recipients', lazy=True))

    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return Message.query.filter_by(recipient=self).filter(
            Message.timestamp > last_read_time).count()


class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.admin


class Message(db.Model):
    message_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(50))
    content = db.Column(db.String(250))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Message {}>'.format(self.body)


admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Message, db.session))
