from slack import WebClient


class SlackClient(object):

    def __init__(self, slack_bot_token):
        self.client = WebClient(slack_bot_token)

    def retrieve_slack_message(self, channel: str, thread_timestamp: str) -> str:
        history = self.client.conversations_history(channel=channel,
                                                    inclusive=True,
                                                    oldest=thread_timestamp,
                                                    limit=1)
        [message] = [m['text'] for m in history['messages'] if m['ts'] == thread_timestamp]
        print(f"Message found: {message}")
        return message

    def reply(self, channel: str, thread_timestamp: str, message: str):
        print(f"Will post '{message}' to channel {channel} into thread with timestamp {thread_timestamp}")
        response = self.client.chat_postMessage(channel=channel,
                                                text=message,
                                                thread_ts=thread_timestamp)
