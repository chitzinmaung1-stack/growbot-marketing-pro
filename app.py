import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# Render Environment Variables ထဲက Key တွေကို ဆွဲယူခြင်း
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")

@app.route('/')
def home():
    # Browser ကနေ ဝင်လိုက်ရင် မြင်ရမည့် Interface
    return """
    <div style="text-align:center; margin-top:50px; font-family:sans-serif;">
        <h1>🚀 GrowBot Marketing Pro Live</h1>
        <p>အောက်ကခလုတ်ကို နှိပ်လိုက်ရင် AI က Content ရေးပြီး Page ပေါ် တိုက်ရိုက်တင်ပေးမှာပါ</p>
        <a href='/test-post'>
            <button style="padding:15px 30px; font-size:18px; cursor:pointer; background-color:#28a745; color:white; border:none; border-radius:5px;">
                Facebook Post အခုတင်မယ်
            </button>
        </a>
    </div>
    """

@app.route('/test-post')
def test_post():
    # Post တင်ချင်တဲ့ Topic ကို ဒီမှာ ပြောင်းနိုင်ပါတယ်
    topic = "AI Chatbot က SME လုပ်ငန်းရှင်တွေအတွက် ဘယ်လောက် အကျိုးရှိလဲ"
    
    # ၁။ Gemini AI နဲ့ Marketing Post ရေးခိုင်းခြင်း
    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GOOGLE_API_KEY}"
    system_instruction = "မင်းက GrowBot Agency ရဲ့ Marketing Pro ဖြစ်တယ်။ AI က ဝန်ထမ်းစရိတ်သက်သာကြောင်း SME တွေအတွက် Facebook Post တစ်ခု မြန်မာလို ရေးပေးပါ။"
    
    try:
        gemini_res = requests.post(gemini_url, json={"contents": [{"parts": [{"text": f"{system_instruction}\nTopic: {topic}"}]}]})
        post_text = gemini_res.json()['candidates'][0]['content']['parts'][0]['text']
        
        # ၂။ AI ပုံဖန်တီးခြင်း (Topic ပေါ်မူတည်ပြီး ပုံထုတ်ပေးပါမယ်)
        image_url = f"https://pollinations.ai/p/AI_Digital_Marketing_Assistant_Professional?width=1024&height=1024&seed=42"
        
        # ၃။ Facebook Page ပေါ်သို့ ပုံနှင့်စာသား တိုက်ရိုက်တင်ခြင်း
        fb_url = f"https://graph.facebook.com/v21.0/me/photos?access_token={PAGE_ACCESS_TOKEN}"
        fb_payload = {
            "url": image_url,
            "caption": post_text
        }
        fb_res = requests.post(fb_url, json=fb_payload)
        
        return f"""
        <div style="text-align:center; font-family:sans-serif;">
            <h2 style="color:green;">✅ အောင်မြင်ပါသည်!</h2>
            <p>Facebook Page မှာ Post တက်သွားပါပြီ။</p>
            <br>
            <a href="/">နောက်ထပ်တင်ရန် ပြန်သွားမည်</a>
        </div>
        """
    except Exception as e:
        return f"<h2 style='color:red;'>Error ဖြစ်သွားပါသည်-</h2><p>{str(e)}</p>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
