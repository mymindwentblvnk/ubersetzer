from slack import WebClient
from translation_client import Language


def create_introduction_block(target_language: Language) -> dict:
    return {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"The following translation into {target_language.value.language} :{target_language.value.flag_emoji}: was triggered by :{target_language.value.emoji}:."  # noqa: E501
        }
    }


def create_feedback_block(admin_slack_channel) -> dict:
    return {
        "type": "context",
        "elements": [
            {
                "type": "mrkdwn",
                "text": f":bulb: If you have feedback, contact us in #{admin_slack_channel}",  # noqa: E501
            }
        ]
    }


def create_divider_block() -> dict:
    return {
        "type": "divider",
    }


def create_translation_block(translation: str) -> dict:
    return {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": translation,
        }
    }


def create_blocks_for_translation(translation: str,
                                  target_language: Language,
                                  admin_slack_channel: str) -> list:
    return [
        create_introduction_block(target_language),
        create_divider_block(),
        create_translation_block(translation),
        create_divider_block(),
        create_feedback_block(admin_slack_channel),
    ]


class SlackClient(object):

    def __init__(self, slack_bot_token):
        self.client = WebClient(slack_bot_token)

    def retrieve_slack_message(self,
                               channel: str,
                               thread_timestamp: str) -> str:
        history = self.client.conversations_history(channel=channel,
                                                    inclusive=True,
                                                    oldest=thread_timestamp,
                                                    limit=1)
        [message] = [m['text'] for m in history['messages'] if m['ts'] == thread_timestamp]  # noqa: E501
        return message

    def reply(self, channel: str, thread_timestamp: str, blocks: list):
        _ = self.client.chat_postMessage(channel=channel,
                                         blocks=blocks,
                                         text="ubersetzer: New translation for a thread you follow.",
                                         thread_ts=thread_timestamp)
