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
accessToken = ''
line_bot_api = LineBotApi(accessToken)
handler = WebhookHandler('')

accessToken1 = ''
line_bot_api1 = LineBotApi(accessToken1)
handler1 = WebhookHandler('')

@app.route("/point", methods=['POST'])
def point():
    import pygsheets
    gc = pygsheets.authorize(service_account_file='testing-dc6ff47816c7.json')
    survey_url = 'https://docs.google.com/spreadsheets/d/'
    sh = gc.open_by_url(survey_url)
    wks1 = sh.worksheet_by_title("pet")
    num = (wks1.rows)+1
    wks1.update_value('A2','testinghere')

@app.route("/callback", methods=['POST'])
#@app.route("/", methods=['POST'])
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


def gameStart(event,userId):
    import datetime
    Dayday = datetime.datetime.now()
    if (Dayday.hour)==4 or ((Dayday.hour)==5 and (Dayday.minute)==0):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="現在你的精靈正在休息、補充體力，請五點之後再玩喔!"))    
    else:
        L = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        ans = random.sample(L, 4)
        random.shuffle(ans)
        A = "%d%d%d%d" % (ans[0], ans[1], ans[2], ans[3])
        temp = [userId, A, 0]
        data.append(temp)
        import pygsheets
        gc = pygsheets.authorize(service_account_file='testing-dc6ff47816c7.json')
        survey_url = 'https://docs.google.com/spreadsheets/d/'
        sh = gc.open_by_url(survey_url)
        wks1 = sh.worksheet_by_title("push")
        num = (wks1.rows)+1
        for i in range(1,num):
            if userId == (wks1.cell((i,1)).value):
                indexList = i
                break
        if int(wks1.cell((indexList,5)).value)>=5:
            line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text="今天已經解5次密碼，為今日上限。\n辛苦你了，現在就該好好休息，帶著折扣，來去夜市犒賞今天的自己"))         
        else:
            wks1.cell((indexList,5)).value = int(wks1.cell((indexList,5)).value)+1
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="遊戲規則-猜數字:\n題目由四個不重複的數字組成:\n若猜的數字有在題目當中且位置不正確為B\n若猜的數字有在題目當中且位置正確則為A\n每次猜測會告訴玩家幾A幾B\n若想結束遊戲，則輸入「退出」。\n開始遊戲!!"))            
def game(index, event,userId):
    global data
    import datetime
    Dayday = datetime.datetime.now()
    if (Dayday.hour)==4 or ((Dayday.hour)==5 and (Dayday.minute)==0):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="現在你的精靈正在休息、補充體力，請五點之後再玩喔!"))
    else:
        A = data[index][1]
    
        s = event.message.text
        b = 0
        a = 0
        print(''.join(A))
        for i in range(4):
            if (s[i]in A):
                b += 1
                if (s[i] == A[i]):
                    a += 1
                    b -= 1
        data[index][2] += 1
        if(a != 4):
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="%dA%dB" % (a, b)))
        else:
            data[index][1] =''
            import pygsheets
            gc = pygsheets.authorize(service_account_file='testing-dc6ff47816c7.json')
            survey_url = 'https://docs.google.com/spreadsheets/d'
            sh = gc.open_by_url(survey_url)
            wks1 = sh.worksheet_by_title("push")
            num = (wks1.rows)+1
            for i in range(1,num):
                if userId == (wks1.cell((i,1)).value):
                    indexList = i
                    break
    
            if (1<=data[index][2]<=5):
                p = int(wks1.cell((indexList,7)).value)
                add = '\n恭喜你獲得一張20元的今日折價券!!!'
                wks1.cell((indexList,7)).value =p +1
            elif (6<=data[index][2]<=12):
                p = int(wks1.cell((indexList,4)).value)            
                add = '\n恭喜你獲得一張10元的今日折價券!!!'
                wks1.cell((indexList,4)).value = p+1
            elif (13<=data[index][2]<=20):
                p = int(wks1.cell((indexList,6)).value)
                add = '\n恭喜你獲得一張5元的今日折價券!!!'
                wks1.cell((indexList,6)).value = p+1
            else:
                add = ''
            wks1.cell((indexList,5)).value = int(wks1.cell((indexList,5)).value)+1                             
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage("Yeah!你總共猜了%d次%s" % (data[index][2],add)))

def gameTime(event):
    sendmsg = FlexSendMessage(
        alt_text='mypet',
        contents={
            "type": "bubble",
            "direction": "ltr",
            "body": {
              "type": "box",
              "layout": "vertical",
              "contents": [
                {
                  "type": "text",
                  "text": "請選擇你想要?",
                  "align": "center"
                },
                {
                  "type": "button",
                  "action": {
                    "type": "message",
                    "label": "使用今日折價券",
                    "text": "我想要使用今日折價券"
                  }
                },
                {
                  "type": "button",
                  "action": {
                    "type": "message",
                    "label": "開始遊戲",
                    "text": "遊戲開始"
                  }
                }
              ]
            }
        }
    )
    line_bot_api.reply_message(event.reply_token,sendmsg)
def useFive(event,userId):
    import pygsheets
    gc = pygsheets.authorize(service_account_file='testing-dc6ff47816c7.json')
    survey_url = 'https://docs.google.com/spreadsheets/d/'
    sh = gc.open_by_url(survey_url)
    wks1 = sh.worksheet_by_title("push")
    num = (wks1.rows)+1
    for i in range(1,num):
        if userId == (wks1.cell((i,1)).value):
            indexList = i
            break
    p = int(wks1.cell((indexList,6)).value)
    if p<=0:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="你目前沒有五元折價券喔!"))
    else:                                
        sendmsg = FlexSendMessage(
            alt_text='fiveUse',
            contents={
                "type": "bubble",
                "direction": "ltr",
                "header": {
                  "type": "box",
                  "layout": "vertical",
                  "contents": [
                    {
                      "type": "text",
                      "text": "使用五元折價券",
                      "align": "center",
                      "weight": "bold",
                      "color": "#00AEFA"
                    }
                  ]
                },
                "body": {
                  "type": "box",
                  "layout": "vertical",
                  "contents": [
                    {
                      "type": "text",
                      "text": "請將此訊息出示給店家，由店家按下確認。",
                      "align": "start",
                      "color": "#000000",
                      "wrap":True
                    }
                  ]
                },
                "footer": {
                  "type": "box",
                  "layout": "horizontal",
                  "contents": [
                    {
                      "type": "button",
                      "action": {
                        "type": "message",
                        "label": "確認",
                        "text": "確認使用五元折價券"
                      },
                      "style": "primary",
                      "gravity": "center"
                    }
                  ]
                }
            }                    
        )
        line_bot_api.reply_message(event.reply_token,sendmsg)  

def confirmFive(event,userId):
    import pygsheets
    gc = pygsheets.authorize(service_account_file='testing-dc6ff47816c7.json')
    survey_url = 'https://docs.google.com/spreadsheets/d/'
    sh = gc.open_by_url(survey_url)
    wks1 = sh.worksheet_by_title("push")
    num = (wks1.rows)+1
    for i in range(1,num):
        if userId == (wks1.cell((i,1)).value):
            indexList = i
            break
    p = int(wks1.cell((indexList,6)).value)
    if p<=0:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="你目前沒有五元折價券喔!"))
    else:
        wks1.cell((indexList,6)).value = p-1
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="已使用一張五元折價券，你目前還有%d張五元折價券"%(p-1)))                    

def useTen(event,userId):
    import pygsheets
    gc = pygsheets.authorize(service_account_file='testing-dc6ff47816c7.json')
    survey_url = 'https://docs.google.com/spreadsheets/d/'
    sh = gc.open_by_url(survey_url)
    wks1 = sh.worksheet_by_title("push")
    num = (wks1.rows)+1
    for i in range(1,num):
        if userId == (wks1.cell((i,1)).value):
            indexList = i
            break
    p = int(wks1.cell((indexList,4)).value)
    if p<=0:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="你目前沒有十元折價券喔!"))
    else:                                
        sendmsg = FlexSendMessage(
            alt_text='TenUse',
            contents={
                "type": "bubble",
                "direction": "ltr",
                "header": {
                  "type": "box",
                  "layout": "vertical",
                  "contents": [
                    {
                      "type": "text",
                      "text": "使用十元折價券",
                      "align": "center",
                      "weight": "bold",
                      "color": "#00AEFA"
                    }
                  ]
                },
                "body": {
                  "type": "box",
                  "layout": "vertical",
                  "contents": [
                    {
                      "type": "text",
                      "text": "請將此訊息出示給店家，由店家按下確認。",
                      "align": "start",
                      "color": "#000000",
                      "wrap":True
                    }
                  ]
                },
                "footer": {
                  "type": "box",
                  "layout": "horizontal",
                  "contents": [
                    {
                      "type": "button",
                      "action": {
                        "type": "message",
                        "label": "確認",
                        "text": "確認使用十元折價券"
                      },
                      "style": "primary",
                      "gravity": "center"
                    }
                  ]
                }
            }                    
        )
        line_bot_api.reply_message(event.reply_token,sendmsg)  

def confirmTen(event,userId):
    import pygsheets
    gc = pygsheets.authorize(service_account_file='testing-dc6ff47816c7.json')
    survey_url = 'https://docs.google.com/spreadsheets/d/'
    sh = gc.open_by_url(survey_url)
    wks1 = sh.worksheet_by_title("push")
    num = (wks1.rows)+1
    for i in range(1,num):
        if userId == (wks1.cell((i,1)).value):
            indexList = i
            break
    p = int(wks1.cell((indexList,4)).value)
    if p<=0:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="你目前沒有十元折價券喔!"))
    else:
        wks1.cell((indexList,4)).value = p-1
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="已使用一張十元折價券，你目前還有%d張十元折價券"%(p-1)))                    


def useTwen(event,userId):
    import pygsheets
    gc = pygsheets.authorize(service_account_file='testing-dc6ff47816c7.json')
    survey_url = 'https://docs.google.com/spreadsheets/d/'
    sh = gc.open_by_url(survey_url)
    wks1 = sh.worksheet_by_title("push")
    num = (wks1.rows)+1
    for i in range(1,num):
        if userId == (wks1.cell((i,1)).value):
            indexList = i
            break
    p = int(wks1.cell((indexList,7)).value)
    if p<=0:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="你目前沒有二十元折價券喔!"))
    else:                                
        sendmsg = FlexSendMessage(
            alt_text='TwenUse',
            contents={
                "type": "bubble",
                "direction": "ltr",
                "header": {
                  "type": "box",
                  "layout": "vertical",
                  "contents": [
                    {
                      "type": "text",
                      "text": "使用二十元折價券",
                      "align": "center",
                      "weight": "bold",
                      "color": "#00AEFA"
                    }
                  ]
                },
                "body": {
                  "type": "box",
                  "layout": "vertical",
                  "contents": [
                    {
                      "type": "text",
                      "text": "請將此訊息出示給店家，由店家按下確認。",
                      "align": "start",
                      "color": "#000000",
                      "wrap":True
                    }
                  ]
                },
                "footer": {
                  "type": "box",
                  "layout": "horizontal",
                  "contents": [
                    {
                      "type": "button",
                      "action": {
                        "type": "message",
                        "label": "確認",
                        "text": "確認使用二十元折價券"
                      },
                      "style": "primary",
                      "gravity": "center"
                    }
                  ]
                }
            }                    
        )
        line_bot_api.reply_message(event.reply_token,sendmsg)  

def confirmTwen(event,userId):
    import pygsheets
    gc = pygsheets.authorize(service_account_file='testing-dc6ff47816c7.json')
    survey_url = 'https://docs.google.com/spreadsheets/d/'
    sh = gc.open_by_url(survey_url)
    wks1 = sh.worksheet_by_title("push")
    num = (wks1.rows)+1
    for i in range(1,num):
        if userId == (wks1.cell((i,1)).value):
            indexList = i
            break
    p = int(wks1.cell((indexList,7)).value)
    if p<=0:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="你目前沒有二十元折價券喔!"))
    else:
        wks1.cell((indexList,7)).value = p-1
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="已使用一張二十元折價券，你目前還有%d張二十元折價券"%(p-1)))                    

def checkUserId(msg,data, userId):
    index = -2
    for i in range(len(data)):
        if data[i][1]=='':
            data.pop(i)
        if data[i][0] == userId:
            index = i
            if(msg=="退出"):
                data.pop(i)
                index = -1
    return index

def isFirst(userId):
    import pygsheets
    gc = pygsheets.authorize(service_account_file='testing-dc6ff47816c7.json')
    survey_url = 'https://docs.google.com/spreadsheets/d/'
    sh = gc.open_by_url(survey_url)
    wks1 = sh.worksheet_by_title("push")
    num = (wks1.rows)+1
    inList =0
    for i in range(1,num):
        if userId == (wks1.cell((i,1)).value):
            inList = 1
            break
    if inList == 0:
        num = random.randint(1, 3)
        wks1.append_table([userId,'%d'%num,0,0,0,0], start='A1', end=None, dimension='ROWS', overwrite=False)   

def buyPet(event,userId):
    import pygsheets
    gc = pygsheets.authorize(service_account_file='testing-dc6ff47816c7.json')
    survey_url = 'https://docs.google.com/spreadsheets/d/'
    sh = gc.open_by_url(survey_url)
    wks1 = sh.worksheet_by_title("push")
    num = (wks1.rows)+1
    for i in range(1,num):
        if userId == (wks1.cell((i,1)).value):
            indexList = i
            break    
    sendmsg = TextSendMessage(text="您還不可以選擇新的精靈喔!")
    if int((wks1.cell((indexList,3)).value))>300:
        sendmsg = TemplateSendMessage(
            alt_text='ImageCarousel template',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://imgur.com/HvlXr3c.jpg',
                        action=MessageAction(
                            label='就決定是你了',
                            text='就決定是你了，獨角獸'
                        )   
                    ),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/rv6aVdX.jpg',
                        action=MessageAction(
                            label='就決定是你了',
                            text='就決定是你了，長頸鹿'
                        )   
                    ),
                    ImageCarouselColumn(
                        image_url='https://imgur.com/61qEipa.jpg',
                        action=MessageAction(
                            label='就決定是你了',
                            text='就決定是你了，鵝'
                        )   
                    )                                                               
                ]
            )
        )
                
    line_bot_api.reply_message(event.reply_token, sendmsg)
        
def myPet(event):
    sendmsg = FlexSendMessage(
        alt_text='mypet',
        contents={
            "type": "bubble",
            "direction": "ltr",
            "body": {
              "type": "box",
              "layout": "vertical",
              "contents": [
                {
                  "type": "text",
                  "text": "請選擇你想要?",
                  "align": "center"
                },
                {
                  "type": "button",
                  "action": {
                    "type": "message",
                    "label": "使用百元折價券",
                    "text": "我想要使用百元折價券"
                  }
                },
                {
                  "type": "button",
                  "action": {
                    "type": "message",
                    "label": "查看寵物狀態",
                    "text": "我想要查看寵物狀態"
                  }
                }
              ]
            }
        }
    )
    line_bot_api.reply_message(event.reply_token,sendmsg)
def petSituation(event,userId):
        import pygsheets
        gc = pygsheets.authorize(service_account_file='testing-dc6ff47816c7.json')
        survey_url = 'https://docs.google.com/spreadsheets/d/'
        sh = gc.open_by_url(survey_url)
        wks1 = sh.worksheet_by_title("push")
        num = (wks1.rows)+1
        for i in range(1,num):
            if userId == (wks1.cell((i,1)).value):
                indexList = i
                break
        sendmsg = TextSendMessage(text="發生錯誤，請再點一次")
        p = int(wks1.cell((indexList,3)).value)
        character = int(wks1.cell((indexList,2)).value)
        if  p>=500:
            if(character==1):
                animal="獨角獸"
                animal_url = "https://imgur.com/epcvTMj.jpg"
            elif(character==2):
                animal="長頸鹿"
                animal_url = "https://i.imgur.com/KGrIRli.jpg"
            elif(character==3):
                animal="鵝"
                animal_url = "https://i.imgur.com/QTzhjqV.jpg"                              
            sendmsg = FlexSendMessage(
                alt_text='timeToSayGoodbye',
                contents={
                    "type": "bubble",
                    "hero": {
                      "type": "image",
                      "url": animal_url,
                      "size": "full",
                      "aspectRatio": "20:13",
                      "aspectMode": "cover",
                      "action": {
                        "type": "uri",
                        "label": "Action",
                        "uri": animal_url
                      }
                    },
                    "body": {
                      "type": "box",
                      "layout": "vertical",
                      "spacing": "md",
                      "contents": [
                        {
                          "type": "text",
                          "text": "是時候說再見了。",
                          "size": "xl",
                          "gravity": "center",
                          "weight": "bold",
                          "wrap": True
                        },
                        {
                          "type": "box",
                          "layout": "vertical",
                          "spacing": "sm",
                          "margin": "lg",
                          "contents": [
                            {
                              "type": "box",
                              "layout": "baseline",
                              "spacing": "sm",
                              "contents": [
                                {
                                  "type": "text",
                                  "text": "嗨，我是%s，謝謝你這段期間的照顧，我已經成為可以獨當一面的精靈了。我要去保護我的家族了，謝謝你，後會有期!\n\n啊!你看那邊來了幾隻需要你照顧的精靈"%animal,
                                  "size": "sm",
                                  "color": "#000000",
                                  "wrap": True
                                }
                              ]
                            },
                            {
                              "type": "button",
                              "action": {
                                "type": "postback",
                                "label": "選擇新精靈",
                                "text": "我要選擇新的精靈",
                                "data": "測試"
                              },
                              "style": "primary"
                            }
                          ]
                        }
                      ]
                    }
                }
            )
            line_bot_api.reply_message(event.reply_token, sendmsg)
        else:
            if character==1:
                if p<250 :
                    sendmsg = FlexSendMessage(
                        alt_text='littleUni',
                        contents={
                            "type": "bubble",
                            "direction": "ltr",
                            "header": {
                              "type": "box",
                              "layout": "vertical",
                              "contents": [
                                {
                                  "type": "text",
                                  "text": "幼年階段",
                                  "align": "center",
                                  "weight": "bold",
                                  "color": "#12508F"
                                }
                              ]
                            },
                            "hero": {
                              "type": "image",
                              "url": "https://i.imgur.com/HvlXr3c.jpg",
                              "size": "full",
                              "aspectRatio": "20:13",
                              "aspectMode": "fit"
                            },
                            "body": {
                              "type": "box",
                              "layout": "vertical",
                              "contents": [
                                {
                                  "type": "text",
                                  "text": "你目前有%d點成長值，再%d點就可以到下一個階段喔!!!"%(p,250-p),
                                  "align": "start",
                                  "wrap": True
                                }
                              ]
                            }
                        }                        
                    )                    
                else: 
                    sendmsg = FlexSendMessage(
                        alt_text='middleUni',
                        contents={
                            "type": "bubble",
                            "direction": "ltr",
                            "header": {
                              "type": "box",
                              "layout": "vertical",
                              "contents": [
                                {
                                  "type": "text",
                                  "text": "青年階段",
                                  "align": "center",
                                  "weight": "bold",
                                  "color": "#12508F"
                                }
                              ]
                            },
                            "hero": {
                              "type": "image",
                              "url": "https://i.imgur.com/iRAgDsH.jpg",
                              "size": "full",
                              "aspectRatio": "20:13",
                              "aspectMode": "fit"
                            },
                            "body": {
                              "type": "box",
                              "layout": "vertical",
                              "contents": [
                                {
                                  "type": "text",
                                  "text": "你目前有%d點成長值，再%d點就可以到下一個階段喔!!!"%(p,500-p),
                                  "align": "start",
                                  "wrap": True
                                }
                              ]
                            }
                        }                        
                    )
            elif character==2:
                if p<250 :
                    sendmsg = FlexSendMessage(
                        alt_text='littleGiraffe',
                        contents={
                            "type": "bubble",
                            "direction": "ltr",
                            "header": {
                              "type": "box",
                              "layout": "vertical",
                              "contents": [
                                {
                                  "type": "text",
                                  "text": "幼年階段",
                                  "align": "center",
                                  "weight": "bold",
                                  "color": "#12508F"
                                }
                              ]
                            },
                            "hero": {
                              "type": "image",
                              "url": "https://i.imgur.com/rv6aVdX.jpg",
                              "size": "full",
                              "aspectRatio": "20:13",
                              "aspectMode": "fit"
                            },
                            "body": {
                              "type": "box",
                              "layout": "vertical",
                              "contents": [
                                {
                                  "type": "text",
                                  "text": "你目前有%d點成長值，再%d點就可以到下一個階段喔!!!"%(p,250-p),
                                  "align": "start",
                                  "wrap": True
                                }
                              ]
                            }
                        }                        
                    )
                else:
                    sendmsg = FlexSendMessage(
                        alt_text='middleGiraffe',
                        contents={
                            "type": "bubble",
                            "direction": "ltr",
                            "header": {
                              "type": "box",
                              "layout": "vertical",
                              "contents": [
                                {
                                  "type": "text",
                                  "text": "青年階段",
                                  "align": "center",
                                  "weight": "bold",
                                  "color": "#12508F"
                                }
                              ]
                            },
                            "hero": {
                              "type": "image",
                              "url": "https://i.imgur.com/PbFIsQX.jpg",
                              "size": "full",
                              "aspectRatio": "20:13",
                              "aspectMode": "fit"
                            },
                            "body": {
                              "type": "box",
                              "layout": "vertical",
                              "contents": [
                                {
                                  "type": "text",
                                  "text": "你目前有%d點成長值，再%d點就可以到下一個階段喔!!!"%(p,500-p),
                                  "align": "start",
                                  "wrap": True
                                }
                              ]
                            }
                        }                        
                    )
            elif character==3:
                if p<250 :
                    sendmsg = FlexSendMessage(
                        alt_text='littleGoose',
                        contents={
                            "type": "bubble",
                            "direction": "ltr",
                            "header": {
                              "type": "box",
                              "layout": "vertical",
                              "contents": [
                                {
                                  "type": "text",
                                  "text": "幼年階段",
                                  "align": "center",
                                  "weight": "bold",
                                  "color": "#12508F"
                                }
                              ]
                            },
                            "hero": {
                              "type": "image",
                              "url": "https://i.imgur.com/61qEipa.jpg",
                              "size": "full",
                              "aspectRatio": "20:13",
                              "aspectMode": "fit"
                            },
                            "body": {
                              "type": "box",
                              "layout": "vertical",
                              "contents": [
                                {
                                  "type": "text",
                                  "text": "你目前有%d點成長值，再%d點就可以到下一個階段喔!!!"%(p,250-p),
                                  "align": "start",
                                  "wrap": True
                                }
                              ]
                            }
                        }                        
                    )
                else :
                    sendmsg = FlexSendMessage(
                        alt_text='littleGoose',
                        contents={
                            "type": "bubble",
                            "direction": "ltr",
                            "header": {
                              "type": "box",
                              "layout": "vertical",
                              "contents": [
                                {
                                  "type": "text",
                                  "text": "青年階段",
                                  "align": "center",
                                  "weight": "bold",
                                  "color": "#12508F"
                                }
                              ]
                            },
                            "hero": {
                              "type": "image",
                              "url": "https://i.imgur.com/sFRjuit.jpg",
                              "size": "full",
                              "aspectRatio": "20:13",
                              "aspectMode": "fit"
                            },
                            "body": {
                              "type": "box",
                              "layout": "vertical",
                              "contents": [
                                {
                                  "type": "text",
                                  "text": "你目前有%d點成長值，再%d點就可以到下一個階段喔!!!"%(p,500-p),
                                  "align": "start",
                                  "wrap": True
                                }
                              ]
                            }
                        }                        
                    )                                
            line_bot_api.reply_message(event.reply_token, sendmsg)
            

def useHundred(event,userId):
    import pygsheets
    gc = pygsheets.authorize(service_account_file='testing-dc6ff47816c7.json')
    survey_url = 'https://docs.google.com/spreadsheets/d/'
    sh = gc.open_by_url(survey_url)
    wks1 = sh.worksheet_by_title("push")
    num = (wks1.rows)+1
    for i in range(1,num):
        if userId == (wks1.cell((i,1)).value):
            indexList = i
            break
    p = int(wks1.cell((indexList,8)).value)
    if p<=0:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="你目前沒有百元折價券喔!"))
    else:                                
        sendmsg = FlexSendMessage(
            alt_text='hundredUse',
            contents={
                "type": "bubble",
                "direction": "ltr",
                "header": {
                  "type": "box",
                  "layout": "vertical",
                  "contents": [
                    {
                      "type": "text",
                      "text": "使用百元折價券",
                      "align": "center",
                      "weight": "bold",
                      "color": "#00AEFA"
                    }
                  ]
                },
                "body": {
                  "type": "box",
                  "layout": "vertical",
                  "contents": [
                    {
                      "type": "text",
                      "text": "請將此訊息出示給店家，由店家按下確認。",
                      "align": "start",
                      "color": "#000000",
                      "wrap":True
                    }
                  ]
                },
                "footer": {
                  "type": "box",
                  "layout": "horizontal",
                  "contents": [
                    {
                      "type": "button",
                      "action": {
                        "type": "message",
                        "label": "確認",
                        "text": "確認使用百元折價券"
                      },
                      "style": "primary",
                      "gravity": "center"
                    }
                  ]
                }
            }                    
        )
        line_bot_api.reply_message(event.reply_token,sendmsg)    
def confirmHundred(event,userId):
    import pygsheets
    gc = pygsheets.authorize(service_account_file='testing-dc6ff47816c7.json')
    survey_url = 'https://docs.google.com/spreadsheets/d/'
    sh = gc.open_by_url(survey_url)
    wks1 = sh.worksheet_by_title("push")
    num = (wks1.rows)+1
    for i in range(1,num):
        if userId == (wks1.cell((i,1)).value):
            indexList = i
            break
    p = int(wks1.cell((indexList,8)).value)
    if p<=0:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="你目前沒有百元折價券喔!"))
    else:
        wks1.cell((indexList,8)).value = p-1
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="已使用一張百元折價券，你目前還有%d張百元折價券"%(p-1)))                    
def pickCoupon(event):    
    sendmsg = FlexSendMessage(
        alt_text='pickCoupon',
        contents={
            "type": "bubble",
            "direction": "ltr",
            "header": {
              "type": "box",
              "layout": "vertical",
              "contents": [
                {
                  "type": "text",
                  "text": "請選擇你要使用的折價券",
                  "align": "center"
                }
              ]
            },
            "footer": {
              "type": "box",
              "layout": "vertical",
              "contents": [
                {
                  "type": "button",
                  "action": {
                    "type": "message",
                    "label": "5元今日折價券",
                    "text": "我要使用一張5元今日折價券"
                  },
                  "gravity": "center"
                },
                {
                  "type": "button",
                  "action": {
                    "type": "message",
                    "label": "10元今日折價券",
                    "text": "我要使用一張10元今日折價券"
                  },
                  "gravity": "center"
                },
                {
                  "type": "button",
                  "action": {
                    "type": "message",
                    "label": "20元今日折價券",
                    "text": "我要使用一張20元今日折價券"
                  },
                  "gravity": "center"
                }
              ]
            }
          }        
        )    
    line_bot_api.reply_message(event.reply_token,sendmsg)    
   



     
data = []  # [[userID, answer, guessTime],[userID, answer, guessTime]]

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.source.user_id !="":        
        global data
        userId = event.source.user_id #getUserId
        index = -2
        isFirst(userId)
        index = checkUserId(event.message.text,data,userId)
        if index == -2:
            msg = event.message.text
            num = random.randint(1, 10)
            guessTime = 1
            if msg == "救救我的選擇障礙吧！":
                text_message = TextSendMessage(text='晚餐你想選什麼呢?\n你想要?',
                                               quick_reply=QuickReply(items=[
                                                   QuickReplyButton(action=MessageAction(label="吃美食",text="吃什麼?")), QuickReplyButton(action=MessageAction(label="喝飲品",text="喝什麼?"))
                                               ]))
                line_bot_api.reply_message(event.reply_token, text_message)
            elif msg == "我想要使用今日折價券":
                pickCoupon(event)
            elif msg == "我要使用一張5元今日折價券":
                useFive(event,userId)
            elif msg == "我要使用一張10元今日折價券":
                useTen(event, userId)
            elif msg == "我要使用一張20元今日折價券":
                useTwen(event, userId)
            elif msg == "確認使用五元折價券":
                confirmFive(event, userId)
            elif msg == "確認使用十元折價券":
                confirmTen(event, userId)
            elif msg == "確認使用二十元折價券":
                confirmTwen(event, userId)
            elif msg == "遊戲TIME":
                gameTime(event)
            elif msg == "遊戲開始":
                gameStart(event,userId)
            elif msg == "我的寵物":
                myPet(event)
            elif msg == "我想要使用百元折價券":
                useHundred(event,userId)
            elif msg == "確認使用百元折價券":
                confirmHundred(event,userId)
            elif msg == "我想要查看寵物狀態":
                petSituation(event,userId)
            elif msg =="吃什麼?":
                randomEat = ['海產粥','方記水餃','林家八寶冰','土魠魚羹']
                ranEatnum = random.randint(0,len(randomEat)-1)  # 隨機吃串列
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=randomEat[ranEatnum]))
            elif msg == "喝什麼?":
                randomDrink = ['鄭老牌木瓜牛奶','檸檬愛玉','排骨酥湯','鮮魚湯']
                ranDrinknum = random.randint(0,len(randomDrink)-1)  # 隨機喝串列
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=randomDrink[ranDrinknum]))
            elif msg == '就決定是你了，獨角獸':
                import pygsheets
                gc = pygsheets.authorize(service_account_file='testing-dc6ff47816c7.json')
                survey_url = 'https://docs.google.com/spreadsheets/d/'
                sh = gc.open_by_url(survey_url)
                wks1 = sh.worksheet_by_title("push")
                num = (wks1.rows)+1
                for i in range(1,num):
                    if userId == (wks1.cell((i,1)).value):
                        indexList = i
                        break
                wks1.cell((indexList,2)).value = 1
                wks1.cell((indexList,3)).value = 0
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="哇~是獨角獸!!!"))
            elif msg == '就決定是你了，鵝':
                import pygsheets
                gc = pygsheets.authorize(service_account_file='testing-dc6ff47816c7.json')
                survey_url = 'https://docs.google.com/spreadsheets/d//'
                sh = gc.open_by_url(survey_url)
                wks1 = sh.worksheet_by_title("push")
                num = (wks1.rows)+1
                for i in range(1,num):
                    if userId == (wks1.cell((i,1)).value):
                        indexList = i
                        break
                wks1.cell((indexList,2)).value = 3
                wks1.cell((indexList,3)).value = 0
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="哇~是鵝!!"))
            elif msg == '就決定是你了，長頸鹿':
                import pygsheets
                gc = pygsheets.authorize(service_account_file='testing-dc6ff47816c7.json')
                survey_url = 'https://docs.google.com/spreadsheets/d/'
                sh = gc.open_by_url(survey_url)
                wks1 = sh.worksheet_by_title("push")
                num = (wks1.rows)+1
                for i in range(1,num):
                    if userId == (wks1.cell((i,1)).value):
                        indexList = i
                        break
                wks1.cell((indexList,2)).value = 2
                wks1.cell((indexList,3)).value = 0
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="哇~是長頸鹿!!!"))
            elif msg == '我要選擇新的精靈':
                buyPet(event,userId)
        elif index == -1:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="遊戲退出"))
        else:
            game(index, event,userId)

if __name__ == "__main__":
#    app.run(port=3000)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
