import datetime

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class SlackReaction(db.Model):

    __tablename__ = 'slack_reaction'
    slack_reaction_id = db.Column(db.Integer, primary_key=True, index=True)
    channel_id = db.Column(db.String, index=True)
    thread_timestamp = db.Column(db.String, index=True)
    reaction = db.Column(db.String, index=True)
    created_at_utc = db.Column(db.DateTime, default=datetime.datetime.utcnow)
