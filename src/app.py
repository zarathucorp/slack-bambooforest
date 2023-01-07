import os
import logging
logging.basicConfig(level=logging.DEBUG)

from slack_bolt import App
from slack_sdk.errors import SlackApiError

from dotenv import load_dotenv
load_dotenv(verbose=True)
SLACK_SIGNING_SECRET = os.getenv('SLACK_SIGNING_SECRET')
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
CHANNEL_NAME=os.getenv("CHANNEL_NAME")

from name import randname

app = App(
    token=SLACK_BOT_TOKEN,
    signing_secret=SLACK_SIGNING_SECRET
)

@app.action("reply")
@app.shortcut("post")
@app.shortcut("reply")
def open_modal(ack, body, shortcut, client, logger, block_actions):
    ack()
    try:
        try:
            try:
                message_ts=body['message_ts']
            except:
                message_ts=body['container']['message_ts']
        except:
            message_ts=""
        result = client.views_open(
            trigger_id=body["trigger_id"],
            view={
                "type": "modal",
                "title": {
                    "type": "plain_text",
                    "text": "대나무숲 포스팅",
                    "emoji": True
                },
                "submit": {
                    "type": "plain_text",
                    "text": "제출",
                    "emoji": True
                },
                "close": {
                    "type": "plain_text",
                    "text": "취소",
                    "emoji": True
                },
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "익명으로 게시글을 남길 수 있는 대나무숲입니다. *한번 글을 남기시면 스스로 삭제할 수 없습니다.*"
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "input",
                        "block_id": "post_input_block",
                        "element": {
                            "type": "plain_text_input",
                            "multiline": True,
                            "action_id": "post_content_input"
                        },
                        "label": {
                            "type": "plain_text",
                            "text": "내용",
                            "emoji": True
                        }
                    },
                    {
                        "type": "input",
                        "block_id": "name_input_block",
                        "element": {
                            "type": "plain_text_input",
                            "action_id": "name_input"
                        },
                        "label": {
                            "type": "plain_text",
                            "text": "이름",
                            "emoji": True
                        },
                        "optional": True
                    }
                ],
                "callback_id": "view_post",
                "private_metadata": message_ts
            }
        )
        logger.info(result)

    except SlackApiError as e:
        logger.error("Error creating conversation: {}".format(e))

@app.view("view_post")
def handle_submission(ack, body, client, view, logger):
    ack()
    logger.info(body)
    message_ts=view['private_metadata']
    content=view['state']['values']['post_input_block']['post_content_input']['value']
    username=view["state"]["values"]["name_input_block"]["name_input"]['value']
    if username is None:
        username=randname()

    if message_ts == "":
        type="게시글"
    else:
        type="댓글"

    send_message=[
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": ":bamboo: 익명 메시지 :bamboo:"
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*{username}님의 {type}입니다.*"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "plain_text",
                            "text": f"{content}"
                        },
                        "accessory": {
                            "type": "button",
                            "action_id": "reply",
                            "text": {
                                "type": "plain_text",
                                "text": "댓글 달기",
                                "emoji": True
                            }
                        }
                    }
                ]

    if message_ts == "":
        client.chat_postMessage(channel=CHANNEL_NAME, blocks=send_message)
    else: 
        client.chat_postMessage(channel=CHANNEL_NAME, thread_ts=message_ts, blocks=send_message)

@app.action("reply")
def actionbutton(ack, say):
    ack()
    say("Good")

if __name__ == "__main__":
    app.start(3000)
