from flask import Flask, request, jsonify,render_template
from PIL import Image
import pytesseract



app = Flask(__name__)

#pytesseract.pytesseract.tesseract_cmd = r"D:\Chung_Hua_University\2024\Tesseract-OCR\tesseract.exe"
@app.route('/')  
def upload():  
    return render_template("index.html")  

@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file'] 
        
        f.save(f.filename)  
        image_data = Image.open(f)

        
        text = pytesseract.image_to_string(image_data, lang="chi_tra+eng")
        print(text)        
        return render_template("success.html", name = text)  


if __name__ == '__main__':
    app.run()