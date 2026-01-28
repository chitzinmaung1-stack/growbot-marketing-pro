import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")

@app.route('/auto-post', methods=['POST'])
def auto_post():
    data = request.get_json()
    topic = data.get('topic', 'AI နည်းပညာရဲ့ အကျိုးကျေးဇူးများ')
    
    # ၁။ AI နဲ့ ဆွဲဆောင်မှုရှိတဲ့ Marketing Content ရေးခိုင်းခြင်း
    system_instruction = """
    မင်းက GrowBot Agency ရဲ့ Marketing Pro ဖြစ်တယ်။ 
    AI က ဝန်ထမ်းစရိတ်သက်သာပြီး ၂၄ နာရီအလုပ်လုပ်နိုင်ကြောင်း SME တွေအတွက် Facebook Post တစ်ခု မြန်မာလို ရေးပေးပါ။
    စာသားထဲမှာ GrowBot Agency နဲ့ ချိတ်ဆက်ဖို့ တိုက်တွန်းချက်ပါရမယ်။
    """
    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GOOGLE_API_KEY}"
    
    try:
        gemini_res = requests.post(gemini_url, json={"contents": [{"parts": [{"text": f"{system_instruction}\nTopic: {topic}"}]}]})
        post_text = gemini_res.json()['candidates'][0]['content']['parts'][0]['text']
        
        # ၂။ AI နဲ့ ပုံဖန်တီးခြင်း (topic ပေါ်မူတည်ပြီး AI ပုံထုတ်ပေးပါမယ်)
        image_query = topic.replace(" ", "_")
        image_url = f"https://pollinations.ai/p/{image_query}?width=1024&height=1024&seed=42"
        
        # ၃။ Facebook Page ပေါ် ပုံနှင့်စာသား တိုက်ရိုက်တင်ခြင်း
        fb_url = f"https://graph.facebook.com/v21.0/me/photos?access_token={PAGE_ACCESS_TOKEN}"
        fb_payload = {
            "url": image_url,
            "caption": post_text
        }
        fb_res = requests.post(fb_url, json=fb_payload)
        
        return jsonify({
            "status": "success", 
            "message": "Post published successfully!",
            "fb_response": fb_res.json()
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
