from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('S7X9UWoHaIh4oXILrCZTSjUj4ngwiZSDt+WMLA/VmA6UG5dxOxRGF8ODOq4H9ZuOYgrTTaDQYN2B6iBIaXEQPwKoJt3uit3anqklTWw1N7MyL4XKOTEsqFn+SvuPv58i31npmgTv5ykduY/T2AaMUAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('7b71a98cfbf44c0ea7f3eb1429148802')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return "ok"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
