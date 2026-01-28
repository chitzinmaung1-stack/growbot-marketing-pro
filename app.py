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
    return "GrowBot Marketing Pro (Gemini 3 + FB Fix) is running!"

@app.route('/telegram-webhook', methods=['POST'])
def telegram_webhook():
    data = request.json
    if "message" in data:
        chat_id = str(data["message"]["chat"]["id"])
        text = data["message"].get("text", "")

        if chat_id == MY_CHAT_ID:
            if text.lower() == "/start":
                send_tg_message("မင်္ဂလာပါ CEO။ Post တင်ခိုင်းချင်ရင် ခေါင်းစဉ် (Topic) ကို ရိုက်ပို့ပေးပါခင်ဗျာ။")
            else:
                send_tg_message(f"'{text}' အတွက် Marketing Post ကို Gemini 3 နဲ့ စရေးနေပါပြီ...")
                
                # Gemini 3 Flash Preview ကို အသုံးပြုထားပါသည်
                gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={GOOGLE_API_KEY}"
                payload = {"contents": [{"parts": [{"text": f"Write a professional Facebook marketing post about {text} in Burmese with emojis."}]}]}
                
                try:
                    res = requests.post(gemini_url, json=payload).json()
                    post_content = res['candidates'][0]['content']['parts'][0]['text']
                    
                    # ပုံဖန်တီးခြင်း
                    image_url = f"https://pollinations.ai/p/business_marketing_{text.replace(' ', '_')}?width=1024&height=1024&seed=123"
                    
                    # Facebook Fix: Deprecated Error ကိုကျော်လွှားရန် /feed endpoint သို့ ပုံနှင့်စာသားတွဲတင်ခြင်း
                    fb_url = f"https://graph.facebook.com/v21.0/me/feed?access_token={PAGE_ACCESS_TOKEN}"
                    fb_payload = {
                        "message": post_content,
                        "link": image_url
                    }
                    fb_res = requests.post(fb_url, json=fb_payload).json()
                    
                    if "id" in fb_res:
                        send_tg_message(f"✅ အောင်မြင်ပါသည်! Facebook မှာ တင်ပြီးပါပြီ။\n\n📄 စာသား:\n{post_content}")
                    else:
                        send_tg_message(f"❌ Facebook API Error: {fb_res}")
                except Exception as e:
                    send_tg_message(f"⚠️ System Error: {str(e)}")
                    
    return "ok", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
