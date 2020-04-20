from flask import Flask, request, abort

from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import random,os

app = Flask(__name__)

accessToken = 'S7X9UWoHaIh4oXILrCZTSjUj4ngwiZSDt+WMLA/VmA6UG5dxOxRGF8ODOq4H9ZuOYgrTTaDQYN2B6iBIaXEQPwKoJt3uit3anqklTWw1N7MyL4XKOTEsqFn+SvuPv58i31npmgTv5ykduY/T2AaMUAdB04t89/1O/w1cDnyilFU='
channelSecret = '7b71a98cfbf44c0ea7f3eb1429148802'
userID ='Ubdf70dbd043a808bbdc15302999fbca1'


line_bot_api = LineBotApi(accessToken)
handler = WebhookHandler(channelSecret)


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

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)

def handle_message(event):
    msg = event.message.text
    num = random.randint(1,10)
    if "抽籤" in msg:
      line_bot_api.reply_message(event.reply_token,TextSendMessage(text="第%d項優惠"%num))
    elif msg =="誰是正妹?":
      line_bot_api.reply_message(event.reply_token,TextSendMessage(text="你就是正妹"))
    else:
        line_bot_api.push_message(userID,1,2)
                
        
if __name__ == "__main__":
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)
