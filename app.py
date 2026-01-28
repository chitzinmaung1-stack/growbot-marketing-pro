import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN") # CEO ရဲ့ Page Token ကို သုံးမှာပါ

@app.route('/')
def home():
    return "GrowBot Marketing Pro is Live & Ready to Post!"

@app.route('/publish-post', methods=['POST'])
def publish_post():
    data = request.get_json()
    topic = data.get('topic', 'AI for SME')
    
    # ၁။ AI နဲ့ Content ရေးခိုင်းခြင်း
    system_instruction = "မင်းက GrowBot Agency ရဲ့ Marketing Pro ဖြစ်တယ်။ AI က ဝန်ထမ်းစရိတ်သက်သာပြီး ၂၄ နာရီအလုပ်လုပ်နိုင်ကြောင်း SME တွေအတွက် Facebook Post တစ်ခု မြန်မာလို ရေးပေးပါ။"
    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GOOGLE_API_KEY}"
    
    try:
        gemini_res = requests.post(gemini_url, json={"contents": [{"parts": [{"text": f"{system_instruction}\nTopic: {topic}"}]}]})
        post_text = gemini_res.json()['candidates'][0]['content']['parts'][0]['text']
        
        # ၂။ ရလာတဲ့ Content ကို Facebook Page ပေါ် တိုက်ရိုက်တင်ခြင်း
        fb_url = f"https://graph.facebook.com/v21.0/me/feed?access_token={PAGE_ACCESS_TOKEN}"
        fb_res = requests.post(fb_url, json={"message": post_text})
        
        return jsonify({"status": "success", "fb_response": fb_res.json()})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
