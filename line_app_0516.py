import os

# 引入套件 flask
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
# 引入 linebot 異常處理
from linebot.exceptions import (
    InvalidSignatureError
)
# 引入 linebot 訊息元件
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, 
    )

app = Flask(__name__)

# LINE_CHANNEL_SECRET 和 LINE_CHANNEL_ACCESS_TOKEN 類似聊天機器人的密碼，記得不要放到 repl.it 或是和他人分享。
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.environ.get('LINE_CHANNEL_SECRET')
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 此為歡迎畫面處理函式，當網址後面是 / 時由它處理
@app.route("/", methods=['GET'])
def hello():
    return 'hello heroku'

# 此為 Webhook callback endpoint處理函式，當網址後面是 /callback 時由它處理
@app.route("/callback", methods=['POST'])
def callback():
    # 取得網路請求的標頭 X-Line-Signature 內容，確認請求是從 LINE Server 送來的
    signature = request.headers['X-Line-Signature']

    # 將請求內容取出
    body = request.get_data(as_text=True)

    # handle webhook body（轉送給負責處理的 handler，ex. handle_message）
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

# decorator 負責判斷 event 為 MessageEvent 實例，event.message 為 TextMessage 實例。所以此為處理 TextMessage 的 handler

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

# __name__ 為內建變數，若程式不是被當作模組引入則為 __main__
if __name__ == "__main__":
    # 運行 Flask server
    app.run()