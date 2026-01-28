import os
import requests
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# Key များ ဆွဲယူခြင်း
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
MY_CHAT_ID = os.getenv("MY_CHAT_ID")

def send_tg_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": MY_CHAT_ID, "text": text})

@app.route('/')
def home():
    return "GrowBot Marketing Pro is running via Telegram!"

# Telegram ဆီက စာလာရင် အလုပ်လုပ်မည့်နေရာ
@app.route('/telegram-webhook', methods=['POST'])
def telegram_webhook():
    data = request.json
    if "message" in data:
        chat_id = str(data["message"]["chat"]["id"])
        text = data["message"].get("text", "")

        # CEO ဆီက စာဟုတ်မဟုတ် စစ်ခြင်း
        if chat_id == MY_CHAT_ID:
            if text.lower() == "/start":
                send_tg_message("မင်္ဂလာပါ CEO။ Post တင်ခိုင်းချင်ရင် ခေါင်းစဉ် (Topic) ကို ရိုက်ပို့ပေးပါခင်ဗျာ။")
            else:
                send_tg_message(f"'{text}' ခေါင်းစဉ်နဲ့ Post ကို AI စရေးနေပါပြီ။ ခဏစောင့်ပေးပါ...")
                
                # ၁။ Gemini AI ဖြင့် Content ရေးခြင်း
                gemini_url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GOOGLE_API_KEY}"
                payload = {"contents": [{"parts": [{"text": f"Write a professional Facebook marketing post about {text} in Burmese with emojis."}]}]}
                
                try:
                    res = requests.post(gemini_url, json=payload).json()
                    post_content = res['candidates'][0]['content']['parts'][0]['text']
                    
                    # ၂။ AI ပုံဖန်တီးခြင်း
                    image_url = f"https://pollinations.ai/p/business_marketing_{text.replace(' ', '_')}?width=1024&height=1024&seed=99"
                    
                    # ၃။ Facebook ပေါ်တင်ခြင်း
                    fb_url = f"https://graph.facebook.com/v21.0/me/photos?access_token={PAGE_ACCESS_TOKEN}"
                    fb_res = requests.post(fb_url, json={"url": image_url, "caption": post_content}).json()
                    
                    if "id" in fb_res:
                        send_tg_message(f"✅ အောင်မြင်ပါသည်! Facebook မှာ တင်ပြီးပါပြီ။\n\n📄 Content:\n{post_content}")
                    else:
                        send_tg_message(f"❌ FB Error: {fb_res}")
                except Exception as e:
                    send_tg_message(f"⚠️ Error: {str(e)}")
                    
    return "ok", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
