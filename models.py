from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class SlackReaction(db.Model):

    __tablename__ = 'slack_reaction'
    channel_id = db.Column(db.String, primary_key=True, index=True)
    thread_timestamp = db.Column(db.String, primary_key=True, index=True)
    reaction = db.Column(db.String, primary_key=True, index=True)
    reaction_count = db.Column(db.Integer, default=1)
