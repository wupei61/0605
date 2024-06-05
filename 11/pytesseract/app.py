from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageMessage
from io import BufferedReader
import pytesseract

#pytesseract.pytesseract.tesseract_cmd = r"D:\Chung_Hua_University\2024\Tesseract-OCR\tesseract.exe"

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
    
    
    message_content = line_bot_api.get_message_content(event.message.id)    
  
    with open('images/'+event.message.id+'.jpg', 'wb') as fd:
        getp=event.message.id
        
        for chunk in message_content.iter_content():            
            fd.write(chunk)
            
    

    with BufferedReader(open('images/'+getp+'.jpg', 'r')) as file:
        print(file)  # -> <_io.BufferedReader name='../data/test.txt'>
        print(file.name)  # -> ../data/test.txt

        image_path = file.name        
        extracted_text = pytesseract.image_to_string(image_path, lang="eng")
        print(extracted_text)      

        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=extracted_text))

  


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