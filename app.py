from decouple import config
from slack_bolt import App

from ubersetzer import Ubersetzer, Language
from slack_api import SlackClient


app = App(token=config('SLACK_BOT_TOKEN'), signing_secret=config('SLACK_SIGNING_SECRET'))
slack_client = SlackClient(config('SLACK_BOT_TOKEN'))
ubersetzer_client = Ubersetzer()


@app.event('reaction_added')
def handle_reaction_added(payload):
    print(payload)
    reaction = payload.get('reaction')

    if reaction == Language.GERMAN.value['slack-reaction']:
        target_language = Language.GERMAN
    elif reaction == Language.ENGLISH.value['slack-reaction']:
        target_language = Language.ENGLISH
    elif reaction == Language.DUTCH.value['slack-reaction']:
        target_language = Language.DUTCH
    else:
        return

    slack_channel = payload.get('item').get('channel')
    slack_thread_timestamp = payload.get('item').get('ts')

    print("Retrieving message that was reacted to")
    message = slack_client.retrieve_slack_message(slack_channel, slack_thread_timestamp)
    translation = ubersetzer_client.translate(message=message, target_language=target_language)

    print("Sending translation back in thread")
    slack_client.reply(channel=slack_channel, thread_timestamp=slack_thread_timestamp, message=translation)


if __name__ == '__main__':
    app.start(port=3000)
