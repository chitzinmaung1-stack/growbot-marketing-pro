import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")

@app.route('/')
def home():
    return """
    <div style="text-align:center; margin-top:50px; font-family:sans-serif;">
        <h1>🚀 GrowBot Marketing Pro</h1>
        <p>Post တင်ရန် အောက်ကခလုတ်ကို နှိပ်ပါ</p>
        <a href='/test-post'><button style="padding:15px 30px; font-size:18px; cursor:pointer; background-color:#28a745; color:white; border:none; border-radius:5px;">Facebook Post အခုတင်မယ်</button></a>
    </div>
    """

@app.route('/test-post')
def test_post():
    topic = "Digital Marketing benefits for SME"
    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GOOGLE_API_KEY}"
    
    # ပိုမိုရိုးရှင်းသော Prompt ကိုသုံးပြီး စမ်းသပ်ခြင်း
    payload = {
        "contents": [{"parts": [{"text": f"Write a short Facebook post about {topic} in Burmese."}]}]
    }
    
    try:
        response = requests.post(gemini_url, json=payload)
        res_json = response.json()
        
        # Error စစ်ဆေးခြင်း
        if 'candidates' not in res_json:
            return f"<h2 style='color:red;'>Gemini Error:</h2><pre>{res_json}</pre>"
            
        post_text = res_json['candidates'][0]['content']['parts'][0]['text']
        image_url = "https://pollinations.ai/p/business_marketing_concept?width=1024&height=1024&seed=50"
        
        fb_url = f"https://graph.facebook.com/v21.0/me/photos?access_token={PAGE_ACCESS_TOKEN}"
        fb_res = requests.post(fb_url, json={"url": image_url, "caption": post_text})
        
        return f"<h2>အောင်မြင်ပါသည်!</h2><p>FB Response: {fb_res.json()}</p>"
    except Exception as e:
        return f"<h2>System Error:</h2><p>{str(e)}</p>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
