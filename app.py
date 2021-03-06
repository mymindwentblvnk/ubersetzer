import logging

from decouple import config
from flask import Flask, request
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler

from models import db, SlackReaction
from translation_client import TranslationClient, Language
from slack_client import SlackClient, create_blocks_for_translation


# Configuration
logging.basicConfig(level=logging.INFO)

# Flask
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL').replace('postgres:', 'postgresql:')  # noqa: E501
# Database
db.init_app(app)
with app.app_context():
    db.create_all()


# Slack Bolt
slack_app = App(token=config('BOT_USER_OAUTH_TOKEN'),
                signing_secret=config('SLACK_SIGNING_SECRET'))
handler = SlackRequestHandler(slack_app)

# Clients
slack_client = SlackClient(config('BOT_USER_OAUTH_TOKEN'))
translation_client = TranslationClient()


def check_if_thread_was_already_translated_and_persist_slack_reaction(channel_id: str,  # noqa: E501
                                                                      thread_timestamp: str,  # noqa: E501
                                                                      reaction: str) -> bool:  # noqa: E501
    with app.app_context():
        # Check if there was any reaction already
        slack_reaction_count = db.session.query(SlackReaction).\
            filter_by(channel_id=channel_id).\
            filter_by(thread_timestamp=thread_timestamp).\
            filter_by(reaction=reaction).\
            count()

        # Persist reaction
        slack_reaction = SlackReaction(channel_id=channel_id,
                                       thread_timestamp=thread_timestamp,  # noqa: E501
                                       reaction=reaction)
        db.session.add(slack_reaction)
        db.session.commit()

        # Return if there was any reaction already
        return slack_reaction_count > 0


@slack_app.event('reaction_added')
def handle_reaction_added(payload):
    logging.info(f"Handling Slack reaction with payload '{payload}'")

    slack_channel = payload.get('item').get('channel')
    slack_thread_timestamp = payload.get('item').get('ts')
    reaction = payload.get('reaction')

    if reaction == Language.GERMAN.value.emoji:
        target_language = Language.GERMAN
    elif reaction == Language.ENGLISH.value.emoji:
        target_language = Language.ENGLISH
    elif reaction == Language.BOSNIAN.value.emoji:
        target_language = Language.BOSNIAN
    elif reaction == Language.SERBIAN.value.emoji:
        target_language = Language.SERBIAN
    elif reaction == Language.CROATIAN.value.emoji:
        target_language = Language.CROATIAN
    elif reaction == Language.DUTCH.value.emoji:
        target_language = Language.DUTCH
    else:
        logging.info(f"Slack reaction '{reaction}' is not supported. "
                     "Reaction will be ignored.")
        return

    # This has to be after the check for allowed reaction emojis
    already_translated = check_if_thread_was_already_translated_and_persist_slack_reaction(channel_id=slack_channel,  # noqa: E501
                                                                                           thread_timestamp=slack_thread_timestamp,  # noqa: E501
                                                                                           reaction=reaction)  # noqa: E501
    if already_translated:
        logging.info("This message was already translated. "
                     "Reaction will still be logged for statistical reasons.")
        return

    logging.info("Retrieving message that was reacted to")
    message = slack_client.retrieve_slack_message(slack_channel,
                                                  slack_thread_timestamp)

    logging.info("Translating message")
    translation = translation_client.translate(message=message,
                                               target_language=target_language)

    logging.info(f"Will post translation to channel {slack_channel} "
                 f"into thread with timestamp {slack_thread_timestamp}")
    slack_blocks = create_blocks_for_translation(translation,
                                                 target_language,
                                                 config('ADMIN_SLACK_CHANNEL'))
    slack_client.reply(channel=slack_channel,
                       thread_timestamp=slack_thread_timestamp,
                       blocks=slack_blocks)


@app.route("/slack/events", methods=["POST"])
def slack_events():
    # SlackRequestHandler translates WSGI requests to Bolt's interface
    # and builds WSGI response from Bolt's response.
    return handler.handle(request)


if __name__ == '__main__':
    app.run(port=3000)
