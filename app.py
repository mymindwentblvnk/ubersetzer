from decouple import config
import logging
from slack_bolt import App

from ubersetzer import Ubersetzer, Language
from slack_api import SlackClient, create_blocks_for_translation


# SLACK_BOT_TOKEN: Bot User OAuth Token
app = App(token=config('SLACK_BOT_TOKEN'),
          signing_secret=config('SLACK_SIGNING_SECRET'))
slack_client = SlackClient(config('SLACK_BOT_TOKEN'))
ubersetzer = Ubersetzer()


@app.event('reaction_added')
def handle_reaction_added(payload):
    logging.info(f"Handling Slack reaction with payload '{payload}'")
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
        return

    slack_channel = payload.get('item').get('channel')
    slack_thread_timestamp = payload.get('item').get('ts')

    logging.info("Retrieving message that was reacted to")
    message = slack_client.retrieve_slack_message(slack_channel,
                                                  slack_thread_timestamp)
    logging.info(f"Message found: {message}")

    logging.info("Translating messag")
    translation = ubersetzer.translate(message=message,
                                       target_language=target_language)

    logging.info(f"Will post '{translation}' to channel {slack_channel} "
                 f"into thread with timestamp {slack_thread_timestamp}")
    slack_blocks = create_blocks_for_translation(translation,
                                                 target_language,
                                                 config('ADMIN_SLACK_CHANNEL'))
    slack_client.reply(channel=slack_channel,
                       thread_timestamp=slack_thread_timestamp,
                       blocks=slack_blocks)


# Initialize Flask app
from flask import Flask, request
flask_app = Flask(__name__)

# SlackRequestHandler translates WSGI requests to Bolt's interface
# and builds WSGI response from Bolt's response.
from slack_bolt.adapter.flask import SlackRequestHandler
handler = SlackRequestHandler(app)

# Register routes to Flask app
@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    # handler runs App's dispatch method
        return handler.handle(request)


if __name__ == '__main__':
    app.start(port=3000)
