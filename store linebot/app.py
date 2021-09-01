from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import*


import os
import json
import random

app = Flask(__name__)
accessToken = 'S7X9UWoHaIh4oXILrCZTSjUj4ngwiZSDt+WMLA/VmA6UG5dxOxRGF8ODOq4H9ZuOYgrTTaDQYN2B6iBIaXEQPwKoJt3uit3anqklTWw1N7MyL4XKOTEsqFn+SvuPv58i31npmgTv5ykduY/T2AaMUAdB04t89/1O/w1cDnyilFU='
line_bot_api = LineBotApi(accessToken)
handler = WebhookHandler('7b71a98cfbf44c0ea7f3eb1429148802')

accessToken1 = 'fEyf2GhueRTjeBlIHy1LMdoKc89htXj6WWm3f8rV6c+bsDpaaaXBTFw9O7WenDsBYo8xaQeWRoRth+/jTsI/F7bGYipezEsJ5IPh6ptsD2TyYmovaQiobQ9gm+J0O+hdiu9iM5F9DpcGGLeupCgBtgdB04t89/1O/w1cDnyilFU='
line_bot_api1 = LineBotApi(accessToken1)
handler1 = WebhookHandler('4ab6c0ad1333c9b94c3d89718e47870c')


@app.route("/store", methods=['POST'])
def store():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler1.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

def checkUserId1(data1, userId1):
    for i in range(len(data1)):
        if data1[i] == userId1:
            return i
    return -1


data1 = [] #[userid]
@handler1.add(MessageEvent, message=TextMessage)
def handle_message1(event):
    global data1
    msg1 = event.message.text
    userId1 = event.source.user_id #getUserId
    index1 = -1
    index1 = checkUserId1(data1,userId1)
    if index1 == -1:
            if msg1 == "我要推播":
                data1.append(userId1)
                line_bot_api1.reply_message(event.reply_token, TextSendMessage(text="請輸入您要推播的內容，或是輸入""取消""以取消推播"))     
    else:
        data1.pop(index1)
        if msg1 == "取消":
            line_bot_api1.reply_message(event.reply_token, TextSendMessage(text="已取消推播"))
        else:
            import pygsheets
            gc = pygsheets.authorize(service_account_file='testing-dc6ff47816c7.json')
            survey_url = 'https://docs.google.com/spreadsheets/d/1jW6jvUXP8aSYcSMh7RDLp1_OXo0Rg4g9fMkFmS90hkM/'
            sh = gc.open_by_url(survey_url)
            wks1 = sh.worksheet_by_title("push")
            num = (wks1.rows)+1
            for i in range(2,num):
                line_bot_api.push_message(wks1.cell((i,1)).value,TextSendMessage(text=msg1))
            line_bot_api1.reply_message(event.reply_token, TextSendMessage(text="已完成推播!"))
    
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
