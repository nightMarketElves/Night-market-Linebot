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
    def googleSheet():
        import gspread
        from oauth2client.service_account import ServiceAccountCredentials
        auth_json_path = 'testing-dc6ff47816c7.json'
        gss_scopes = ['https://spreadsheets.google.com/feeds']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(auth_json_path,gss_scopes)
        gss_client = gspread.authorize(credentials)
        spreadsheet_key = '1jW6jvUXP8aSYcSMh7RDLp1_OXo0Rg4g9fMkFmS90hkM'
        def getAns(ans):
            sheet = gss_client.open_by_key(spreadsheet_key).sheet1
            sheet.update_acell(1,2,ans) 
        
         
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    num = random.randint(1,10)
    global guessTime
    if "抽籤" in msg:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="第%d項優惠"%num))
    elif msg =="誰是正妹?":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="不是你"))
    elif msg == "遊戲開始":
        L=[0,1,2,3,4,5,6,7,8,9]
        ans = random.sample(L,4)
        random.shuffle(ans) 
        global A
        A = "%d%d%d%d"%(ans[0],ans[1],ans[2],ans[3])
        guessTime = 1
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入本次答案"))
    s = msg
    b=0
    a = 0
    for i in range(4):
        if (s[i]in A) :
            b+=1
            if (s[i]==A[i]):
                a+=1
                b-=1
    guessTime+=1
    if(a!=4):
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="%s%dA%dB"%(A,a,b)))
    else:
        line_bot_api.reply_message(event.reply_token,TextSendMessage("yeah你總共猜了%d次"%(guessTime)))
if __name__ == "__main__":
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)
