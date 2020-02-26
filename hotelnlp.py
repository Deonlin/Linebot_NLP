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
from sklearn.externals import joblib
from bert_serving.client import BertClient
import json
import requests

app = Flask(__name__)


clf2 = joblib.load('cls2.pkl')


def sentToVect(sent1, List=None):
    bc = BertClient()
    if List is None:
        List = []
        List.append(sent1)
    sents_enc = bc.encode(List)
    return sents_enc


'''for more details please see https://ithelp.ithome.com.tw/articles/10217767'''
'''Web server目前先用ngrok做架設'''


# import your Line developer channel access token
line_bot_api = LineBotApi(
    'Bag0LXKvWSDAhvFjcY1kXTCfGoMuYeBNDDiJOnKbA1cGi/bRccjkWs5Ha2ST4uXeOps3hkuIEyMs0gcMP6i8Fde/91+nmaJv3ywMSTo2cCzuGA1lTGKjoAeQCpC7voLkvOz5IYAyDj8lrNvxPaQH3AdB04t89/1O/w1cDnyilFU=')
# import your LINE developers channel secret code
handler = WebhookHandler('9859ce7d5e04ac171ba276c689d53990')

# for receive LINE message and return OK to LINE server
@app.route("/api/LineLUIS", methods=['POST'])
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
    question = event.message.text
    result = clf2.predict(sentToVect(question))
    classes = ['房內服務行為', '詢問健身房地點', '詢問餐廳開放時間', '詢問餐廳地點']
    replyIntent = classes[result[0]]
    print(replyIntent)

    # reply content
    class ReplytoClient:
        item1 = f'根據您說的內容，小助手判定是"{replyIntent}"\n收到!!我已聯繫房務人員前來服務，請您稍後一下喔！'
        item2 = f'根據您說的內容，小助手判定是"{replyIntent}"\n健身房位置位於：本飯店B棟第 32 樓層\n歡迎您於開放時間前往，祝您運動愉快！'
        item3 = f'根據您說的內容，小助手判定是"{replyIntent}"\n餐廳開放時間為：早上06:00至晚間22:00\n歡迎您於開放時間前往用餐！'
        item4 = f'根據您說的內容，小助手判定是"{replyIntent}"\n餐廳地點為：本飯店A棟第 2 樓層\n歡迎您於開放時間前往用餐，房客均有用餐優先權!'
        item00 = '對不起，小助手不太了解您問的問題，將直接與服務人員聯繫，為您提供即時服務，請稍等一下喔！'

    if (replyIntent == '房內服務行為'):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=ReplytoClient.item1)
        )
    elif(replyIntent == '詢問健身房地點'):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=ReplytoClient.item2)
        )
    elif(replyIntent == '詢問餐廳開放時間'):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=ReplytoClient.item3)
        )
    elif(replyIntent == '詢問餐廳地點'):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=ReplytoClient.item4)
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=ReplytoClient.item00)
        )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050)
