from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageMessage
import easyocr
from io import BufferedReader


app = Flask(__name__)
line_bot_api = LineBotApi('LINE_CHANNEL_ACCESS_TOKEN')
line_handler = WebhookHandler('LINE_CHANNEL_SECRET')

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@line_handler.add(MessageEvent, message=ImageMessage)
def handle_message(event):
    reader = easyocr.Reader(['ch_tra','en'])    
    
    
    message_content = line_bot_api.get_message_content(event.message.id)    
  
    with open('images/'+event.message.id+'.jpg', 'wb') as fd:
        getp=event.message.id
        
        for chunk in message_content.iter_content():            
            fd.write(chunk)
            
    

    with BufferedReader(open('images/'+getp+'.jpg', 'r')) as file:
        print(file)  # -> <_io.BufferedReader name='../data/test.txt'>
        print(file.name)  # -> ../data/test.txt

        reader = easyocr.Reader(['en'])
        text = reader.readtext(file.name)
        for item in text:       
            print(item[1])
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=item[1]))

  


@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):        

    if event.message.text == "1":        
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='a'))       

       
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="b"))

if __name__ == "__main__":
    app.run()